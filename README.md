# Multimodal RAG System

This is a prototype hybrid Retrieval-Augmented Generation (RAG) system capable of ingesting and structuring information from multiple modalities — starting with text — and storing knowledge in a queryable graph database.

# Features

- Entity and relationship extraction using LLMs (OpenAI GPT-3.5)
- Neo4j-based knowledge graph for relationship mapping
- Modular project structure ready for multimodal extension (image, audio, video)
- Ready for integration with vector search and hybrid retrieval

# Demo Example

Input:
> Andre Achtar-Zadeh is a software engineer at OpenAI. He works on natural language models and AI systems.

Output:
- Extracted Entities: `["Andre Achtar-Zadeh", "OpenAI"]`
- Relationship: `["Andre Achtar-Zadeh", "works_at", "OpenAI"]`
- Graph inserted and visualized in Neo4j

# Setup Instructions

1. Clone the repo:
   ```bash
   git clone https://github.com/chromehollow/multimodal-rag.git
   cd multimodal-rag
