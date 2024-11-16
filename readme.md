# Intro to LLMs and RAG Systems Workshop

This repository contains an educational implementation of a Retrieval-Augmented Generation (RAG) system, designed to demonstrate core concepts of working with Large Language Models (LLMs) and document retrieval. This project is intended for learning purposes and serves as a hands-on introduction to RAG systems.

## 🎯 Educational Objectives

- Understand the basic components of a RAG system
- Learn about embedding-based semantic search
- Explore PDF processing and text chunking
- Implement vector similarity search
- Work with LLMs through the Ollama API
- Build a simple GUI for RAG interactions

## 🚀 Features

- PDF document processing and text extraction
- Sentence-based text chunking
- Semantic search using embeddings
- Integration with Ollama for LLM interactions
- Both console-based and GUI interfaces
- Real-time document question-answering

## 📋 Prerequisites

- Python 3.10+
- Ollama installed and running locally
- Required Python packages:
  - pymupdf
  - numpy
  - tkinter (for GUI version)
  - ollama (Python client)
  - ollama-gui (GUI client)

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/BAW2501/LLM-RAG-WorkshopCode.git
cd LLM-RAG-WorkshopCode
```

2. Install required packages:
```bash
pip install pymupdf numpy ollama-python ollama-gui
```

3. Ensure Ollama is installed and running with required models:
```bash
# Install Ollama (if not already installed)
# Visit https://ollama.ai for installation instructions

# Pull required models
ollama pull llama3.2:3b
ollama pull mxbai-embed-large
```

## 💻 Usage

### Console Version
```bash
python ConsoleBasedRag.py
```

### GUI Version
```bash
python TkinterRAG.py
```

## 🏗️ Project Structure

```
├── ConsoleBasedRag.py    # Console-based implementation
├── TkinterRAG.py         # RAG GUI implementation
└── TkinterLLM.py         # LLM GUI implementation 
└── Visualizations        # Folder for visualisation content 
```

### Key Components

- **PDFProcessor**: Handles PDF text extraction and chunking
- **EmbeddingService**: Manages text embedding generation
- **SemanticSearch**: Implements similarity search functionality
- **QueryProcessor**: Processes user queries and manages LLM interactions
- **RAGSystem**: Orchestrates the entire RAG pipeline
- **RagUI**: Provides a graphical user interface

## ⚙️ Configuration

Key configuration settings can be modified in the `Config` class:
- `CHUNK_SIZE`: Size of text chunks (default: 500)
- `VAULT_FILE`: Storage location for processed text
- `SYSTEM_PROMPT`: Default system prompt for LLM

## 🎓 Workshop Notes

This implementation is designed for educational purposes and includes several simplifications:
- Basic error handling
- In-memory vector storage
- Simple similarity search
- Basic text chunking strategy

These simplifications make the code more accessible for learning but should be enhanced for production use.

## 🚧 Limitations

- Not optimized for large documents
- Basic embedding caching
- Simple chunking strategy
- Limited error handling
- Requires local Ollama installation

## 📚 Learning Resources

To learn more about RAG systems and LLMs:
- [3B1B Playlist On AI](https://www.youtube.com/playlist?list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi)
- [Hands on LLM Book](https://www.goodreads.com/book/show/210408850-hands-on-large-language-models)
- [What is RAG?](https://www.pinecone.io/learn/retrieval-augmented-generation/)
- [RAG Explained in 8 Minutes](https://www.youtube.com/watch?v=HREbdmOSQ18)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)

## ⚖️ License

This project is for educational purposes. Feel free to use and modify for learning and teaching.

## 🤝 Contributing

This is an educational project, but suggestions for improvements that maintain its teaching focus are welcome:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---
*Note: This implementation is designed for learning and demonstration purposes. For production use, consider using established frameworks like LangChain or LlamaIndex.*