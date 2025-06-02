import sys
import os
import json
import datetime as dt

from dotenv import load_dotenv
from openai import OpenAI

from ingestion.auto_ingestor import auto_ingest
from knowledge_graph.entity_extractor import parse_entities
from knowledge_graph.graph_builder import GraphBuilder
from vectorstore.qdrant_handler import (
    init_qdrant,
    clear_qdrant,
    upsert_text,
    search_similar,
)
from hybrid.hybrid_retriever import hybrid_retrieve

# Load environment variables and initialise OpenAI client
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python main.py <file_path> <search_query>")
        sys.exit(1)

    file_path, search_query = sys.argv[1], sys.argv[2]
    if not os.path.exists(file_path):
        sys.exit(f"Error: File not found: {file_path}")

    # 1. Ingest
    print(f"Extracting text from: {file_path}")
    text = auto_ingest(file_path)
    print("Text sample:", text[:500].replace("\n", " "), "...")

    # 2. Vector store
    print("Initialising Qdrant and resetting collection")
    init_qdrant()
    try:
        clear_qdrant()
    except Exception as e:
        print(f"Warning: clear_qdrant skipped ({e})")
    upsert_text(text)

    # 3. Entity and relationship extraction
    print("Extracting entities and relationships")
    raw_entities = parse_entities(text)
    entities_data = (
        json.loads(raw_entities) if isinstance(raw_entities, str) else raw_entities
    )

    # 4. Domain classification
    sample = text[:4000]  # Limit prompt size
    domain_prompt = (
        "Classify the following text into ONE high-level domain "
        "(finance, legal, medical, AI, general):\n\n"
        f"{sample}\n\nDomain:"
    )
    domain_resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": domain_prompt}],
        temperature=0,
    )
    domain_tag = domain_resp.choices[0].message.content.strip()

    # 5. Knowledge graph population
    builder = GraphBuilder()
    builder.add_entities_and_relationships(
        entities_data.get("entities", []),
        entities_data.get("relationships", []),
        source=os.path.basename(file_path),
    )

    # 6. Retrieval
    print("Running similarity search and hybrid retrieval")
    vector_results = search_similar(search_query)
    hybrid_results = hybrid_retrieve(search_query)

    # 6b. Generate final answer using OpenAI with context
    system_prompt = (
        "You are a helpful assistant. Use the retrieved context to answer the query concisely. "
        "If context is not enough, say you don't know."
    )
    context = "\n".join(hybrid_results.get("vector_results", [])) + "\n" + json.dumps(hybrid_results.get("graph_results", []))

    answer_prompt = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{context}\n\nQ: {search_query}"}
    ]

    answer_resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=answer_prompt,
        temperature=0
    )
    final_answer = answer_resp.choices[0].message.content.strip()

    # 7. Consolidate and persist results
    os.makedirs("results", exist_ok=True)
    output = {
        "source_file": file_path,
        "timestamp": dt.datetime.now().isoformat(),
        "domain_tag": domain_tag,
        "entities": entities_data.get("entities", []),
        "relationships": entities_data.get("relationships", []),
        "vector_results": hybrid_results.get("vector_results", vector_results),
        "graph_results": hybrid_results.get("graph_results", []),
        "final_answer": final_answer,
    }

    with open("results/hybrid_results.json", "w") as f:
        json.dump(output, f, indent=2)

    builder.close()
    print("Pipeline complete. Results saved to results/hybrid_results.json")


if __name__ == "__main__":
    main()