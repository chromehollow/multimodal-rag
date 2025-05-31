from vectorstore.qdrant_handler import search_similar
from knowledge_graph.graph_builder import GraphBuilder

def hybrid_retrieve(query, top_k=3):
    print("Running vector search...")
    vector_results = search_similar(query, top_k)
    texts = [res.payload["text"] for res in vector_results]

    print("Running graph search...")
    builder = GraphBuilder()
    entity_matches = builder.find_related_entities(query)
    builder.close()

    return {
        "vector_results": texts,
        "graph_results": entity_matches
    }
