from ingestion.text_ingestor import extract_text
from ingestion.audio.audio_ingestor import transcribe_audio
from knowledge_graph.entity_extractor import parse_entities
from knowledge_graph.graph_builder import GraphBuilder
from vector_store.embedding import embed_text
from vectorstore.qdrant_handler import init_qdrant, upsert_text, search_similar
from ingestion.auto_ingestor import auto_ingest
from hybrid.hybrid_retriever import hybrid_retrieve
import json

def main():
    file_path = "assets/Aiinfo.mp4"

    print("Extracting text from input file...")
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

    print("Executing hybrid retrieval pipeline...")
    results = hybrid_retrieve("Andre Achtar-Zadeh")
    print("Vector Results:", results["vector_results"])
    print("Graph Results:", results["graph_results"])

    builder.close()
    print("Pipeline execution complete.")

if __name__ == "__main__":
    main()
