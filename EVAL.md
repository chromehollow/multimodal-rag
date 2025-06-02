# Evaluation Framework for Multimodal-RAG

This document outlines the evaluation methodology and metrics used to validate the performance and correctness of the Multimodal-RAG system. The system supports retrieval-augmented generation (RAG) across multiple modalities including text, audio, images, and video. Evaluation focuses on two primary components: information extraction and hybrid retrieval quality.

---

## 1. Evaluation Objectives

The goal of the evaluation framework is to answer the following:

- Does the system correctly extract entities and relationships from diverse input modalities?
- Can the system retrieve semantically similar or contextually relevant content across modalities?
- Are the outputs of the system grounded in accurate vector and knowledge-graph representations?

---

## 2. Modalities and Supported Ingestion

| Modality | Ingestion Method | Output Target |
|----------|------------------|----------------|
| Text     | Raw `.txt` files | Entity/Relationship + Embedding |
| Audio    | `.mp3`, `.wav` via ASR | Transcribed text → Entity/Relationship + Embedding |
| Image    | `.png`, `.jpg` via OCR | Extracted text → Entity/Relationship + Embedding |
| Video    | `.mp4` via audio track extraction | Transcribed text → Entity/Relationship + Embedding |

---

## 3. Evaluation Metrics

### 3.1 Entity Extraction Accuracy

- **Definition**: Measures the accuracy of named entities and relationship extraction by the LLM from each modality.
- **Method**: Compare LLM-extracted entities and relationships with manually curated ground truth.
- **Metric**: Exact Match Accuracy and F1-Score.
- **Validation**:
  - Construct expected output for known input files.
  - Validate that system output matches expected entities and relationship tuples.

### 3.2 Vector Similarity Retrieval

- **Definition**: Validates semantic search via vector embeddings in Qdrant.
- **Metric**:
  - Top-1 Recall: Whether the most relevant document appears at rank 1.
  - Top-k Recall (k=3, 5): Whether the correct match is present in the top-k results.
  - Cosine similarity scores for all retrieved matches.
- **Method**:
  - For each query, check if the ground truth match is retrieved and ranked correctly.
  - Use controlled test queries from each modality.

### 3.3 Knowledge Graph Retrieval Precision

- **Definition**: Tests the precision of graph search by verifying correctness of nodes and edges returned from Neo4j.
- **Metric**:
  - Edge Precision: Percentage of returned relationships that are correct.
  - Node Precision: Percentage of returned entities that are valid.
- **Method**:
  - Insert known graph data.
  - Execute structured graph queries and compare results with expected answers.

### 3.4 Hybrid Retrieval Effectiveness

- **Definition**: Measures the combined effectiveness of vector search and knowledge graph search.
- **Metric**: 
  - Relevance overlap score: Jaccard or precision-based overlap between vector and graph outputs.
  - Hybrid Hit Rate: Whether either or both paths (vector/graph) retrieve expected content.
- **Method**:
  - Run hybrid retrieval with predefined queries.
  - Score each component individually, then evaluate combined result relevance.

---

## 4. Test Case Design

Unit tests have been written to validate the functionality of:

- Entity extraction
- Relationship parsing and graph construction
- Vector similarity search in Qdrant
- Graph search in Neo4j
- Hybrid pipeline retrieval

All test cases are located in `tests/test_eval.py`.

To execute:

```bash
python3 -m unittest tests/test_eval.py
