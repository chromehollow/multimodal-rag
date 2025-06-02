# Multimodal RAG System

This is a prototype hybrid Retrieval-Augmented Generation (RAG) system that ingests information from multiple file types and builds a knowledge graph with hybrid search.

## Features

- Multimodal ingestion: `.txt`, `.png`, `.pdf`, `.mp3`, `.mp4`
- Entity and relationship extraction using OpenAI GPT-3.5
- Neo4j graph database for structured relationship mapping
- Qdrant vector database for similarity search
- Hybrid retrieval combining vector and graph results
- Modular architecture (extensible to other modalities)
- Outputs JSON-based results for evaluation

## Example

**Input:**
```
Andre Achtar-Zadeh is a software engineer at OpenAI.
```

**Output:**
```json
{
  "entities": ["Andre Achtar-Zadeh", "OpenAI"],
  "relationships": [["Andre Achtar-Zadeh", "works_at", "OpenAI"]]
}
```

These outputs are inserted into Neo4j and indexed in Qdrant.

## Modalities Tested

| File              | Type  | Text Extraction | Entity Extraction | Graph Insert | Vector Insert |
|-------------------|-------|------------------|--------------------|--------------|----------------|
| sample_text.txt   | Text  | Yes              | Yes                | Yes          | Yes            |
| sample_image.png  | Image | Yes              | Yes                | Yes          | Yes            |
| sample_pdf.pdf    | PDF   | Yes              | Yes                | Yes          | Yes            |
| sample_audio.mp3  | Audio | Yes              | Yes                | Yes          | Yes            |
| Aiinfo.mp4        | Video | Yes              | Yes                | Yes          | Yes            |

Output results are saved to: `results/hybrid_results.json`

## Setup

Clone the repository:
```bash
git clone https://github.com/chromehollow/multimodal-rag.git
cd multimodal-rag
```

Create a virtual environment and install dependencies:
```bash
python3 -m venv venv311
source venv311/bin/activate
pip install -r requirements.txt
```

Run the pipeline:
```bash
python main.py assets/your_file_here.ext "your query here"
```

Make sure Neo4j and Qdrant are running locally. Also, export your OpenAI API key:
```bash
export OPENAI_API_KEY=your_key_here
```
