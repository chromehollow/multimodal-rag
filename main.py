import sys
import json
from ingestion.auto_ingestor import auto_ingest
from knowledge_graph.entity_extractor import parse_entities
from knowledge_graph.graph_builder import GraphBuilder
from vectorstore.qdrant_handler import init_qdrant, upsert_text, search_similar
from hybrid.hybrid_retriever import hybrid_retrieve

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

    print("Inserting entities and relationships into Neo4j...")
    builder = GraphBuilder()
    builder.add_entities_and_relationships(data["entities"], data["relationships"])

    print("Running similarity search on Qdrant...")
    results = search_similar(text)
    print("Top vector result:", results[0])

    print(f"Executing hybrid retrieval for: {search_query}")
    results = hybrid_retrieve(search_query)
    print("Vector Results:", results["vector_results"])
    print("Graph Results:", results["graph_results"])

    with open("results/hybrid_results.json", "w") as f:
        json.dump(results, f, indent=2)

    builder.close()
    print("Pipeline execution complete. Results saved to results/hybrid_results.json")

if __name__ == "__main__":
    main()
