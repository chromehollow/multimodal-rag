import sys
import json
import os
import datetime
from ingestion.auto_ingestor import auto_ingest
from knowledge_graph.entity_extractor import parse_entities
from knowledge_graph.graph_builder import GraphBuilder
from vectorstore.qdrant_handler import init_qdrant, upsert_text, search_similar
from hybrid.hybrid_retriever import hybrid_retrieve
from openai import OpenAI
from dotenv import load_dotenv

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <file_path> <search_query>")
        sys.exit(1)

    file_path = sys.argv[1]
    search_query = sys.argv[2]

    print(f"Extracting text from: {file_path}")
    text = auto_ingest(file_path)
    print("Text extracted:", text[:500], "...")

    print("Initializing Qdrant and inserting vector...")
    init_qdrant()
    upsert_text(text)

    print("Running entity and relationship extraction...")
    raw = parse_entities(text)
    print("LLM response:")
    print(raw)

    print("Parsing extracted JSON data...")
    data = json.loads(raw)

    # Add metadata
    data["source_file"] = file_path
    data["timestamp"] = datetime.datetime.now().isoformat()

    # Load OpenAI key for domain tagging
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Generate domain tag
    domain_prompt = f"Classify this text into a high-level domain like finance, legal, medical, AI, or general:\n\n{text}\n\nDomain:"
    domain_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": domain_prompt}],
        temperature=0
    )
    data["domain_tag"] = domain_response.choices[0].message.content.strip()

    print("Inserting entities and relationships into Neo4j...")
    builder = GraphBuilder()
    builder.add_entities_and_relationships(data["entities"], data["relationships"])

    print("Running similarity search on Qdrant...")
    results = search_similar(text)
    print("Top vector result:", results[0])

    print(f"Executing hybrid retrieval for: {search_query}")
    hybrid_results = hybrid_retrieve(search_query)
    print("Vector Results:", hybrid_results["vector_results"])
    print("Graph Results:", hybrid_results["graph_results"])

    # Merge metadata and hybrid search results
    final_output = {
        **data,
        "vector_results": hybrid_results["vector_results"],
        "graph_results": hybrid_results["graph_results"]
    }

    with open("results/hybrid_results.json", "w") as f:
        json.dump(final_output, f, indent=2)

    builder.close()
    print("Pipeline execution complete. Results saved to results/hybrid_results.json")

if __name__ == "__main__":
    main()
