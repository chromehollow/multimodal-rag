from ingestion.text_ingestor import extract_text
from knowledge_graph.entity_extractor import parse_entities
from knowledge_graph.graph_builder import GraphBuilder
from vector_store.embedding import embed_text
from vectorstore.qdrant_handler import init_qdrant, upsert_text, search_similar
from hybrid.hybrid_retriever import hybrid_retrieve
import json

def main():
    print("Extracting text...")
    text = extract_text("assets/sample.txt")
    print("Text extracted:", text[:80] + "...")

    init_qdrant()
    upsert_text(text)

    print("Running entity parser...")
    raw = parse_entities(text)
    print("LLM response:")
    print(raw)

    print("Parsing JSON...")
    data = json.loads(raw)

    print("Inserting into graph...")
    builder = GraphBuilder()
    builder.add_entities_and_relationships(data["entities"], data["relationships"])

    print("Searching for similar texts...")
    results = search_similar(text)
    print("Top result:", results[0])

    print("Running hybrid retrieval...")
    results = hybrid_retrieve("Andre Achtar-Zadeh")
    print("Vector Results:", results["vector_results"])
    print("Graph Results:", results["graph_results"])

    builder.close()
    print("Done.")

if __name__ == "__main__":
    main()
