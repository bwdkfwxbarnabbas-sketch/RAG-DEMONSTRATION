# RAG Demonstration & Scientific Assistant

A local Retrieval-Augmented Generation (RAG) application built with Python, LangChain, and ChromaDB. This project serves as the foundational architecture for an advanced, agentic reasoning assistant designed to tackle complex technical and scientific problem-solving.

## 🚀 Features

* **Dual-Chain Pattern**: Separates query optimization (rewriting/transformation) from response generation to dramatically improve retrieval accuracy.
* **Persistent Vector Storage**: Utilizes ChromaDB with smart add-and-load logic to manage local data efficiently.
* **Document Processing**: Integrated PDF parsing for local domain-specific knowledge bases.

---

## 📁 Project Structure

```text
aiagents/
├── guides/              # Source PDF documents for the RAG knowledge base
├── chroma_db/           # Local vector database storage (ignored by git)
├── myenv/               # Python virtual environment (ignored by git)
├── main.py              # Main execution script for the RAG pipeline
├── vector.py            # Vector embedding and database indexing logic
├── requirements.txt     # Python package dependencies
└── .gitignore           # Git ignore configuration
