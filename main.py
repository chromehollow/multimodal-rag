from ingestion.text_ingestor import extract_text
from knowledge_graph.entity_extractor import parse_entities
from knowledge_graph.graph_builder import GraphBuilder
import json

print("Extracting text...")
text = extract_text("assets/sample.txt")
print("Text extracted:", text[:80] + "...")

print("Running entity parser...")
raw = parse_entities(text)
print("LLM response:")
print(raw)

print("Parsing JSON...")
data = json.loads(raw)

print("Inserting into graph...")
builder = GraphBuilder()
builder.add_entities_and_relationships(data["entities"], data["relationships"])
builder.close()

print("Done.")
