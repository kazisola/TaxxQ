# TaxXQ 🇺🇸

**An AI-powered tax question-answering application built with Retrieval-Augmented Generation (RAG).**

TaxXQ helps users find answers to common U.S. federal tax questions using information retrieved from tax documents. Instead of relying entirely on an LLM's existing knowledge, it retrieves relevant document content from a Pinecone vector database and passes that context to an LLM to generate an answer.

## Features

- **PDF Document Ingestion:** Upload tax documents in PDF format for processing.
- **Document Processing:** Extract text from PDFs and split it into smaller chunks using LangChain.
- **Vector Embeddings:** Convert document chunks into numerical representations using Google's Gemini embedding model.
- **Semantic Search:** Store and search document vectors in Pinecone to retrieve relevant information based on a user's question.
- **AI-Powered Answers:** Use a Groq-hosted LLM to generate answers grounded in retrieved tax information.
- **Source Tracking:** Return document sources alongside answers to help users identify where information came from.
- **Context-Grounded Responses:** Instruct the LLM to avoid speculation when the retrieved context does not contain enough information.

## How It Works

TaxXQ uses two main pipelines: document ingestion and question answering.

### 1. Document Ingestion

Documents are processed and indexed once so they can be reused across multiple user queries.

```text
PDF Upload
    ↓
PyPDFLoader
    ↓
Text Extraction
    ↓
Recursive Character Text Splitter
    ↓
Document Chunks
    ↓
Gemini Embeddings
    ↓
Pinecone Vector Database
```

### 2. Question Answering

When a user submits a question, TaxXQ searches the existing document collection for relevant content and uses it to generate an answer.

```text
User Question
    ↓
Query Embedding
    ↓
Pinecone Similarity Search
    ↓
Relevant Document Chunks
    ↓
Prompt + Retrieved Context
    ↓
Groq LLM
    ↓
Answer + Sources
```

Documents do not need to be uploaded again for every question. The application can reuse previously indexed content as long as the vectors remain available and the query pipeline is connected to the same index.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| FastAPI | API framework and file-upload handling |
| LangChain | Document processing and RAG pipeline |
| PyPDFLoader | Extract text and metadata from PDFs |
| RecursiveCharacterTextSplitter | Split documents into manageable chunks |
| Google Gemini Embeddings | Convert text into vectors |
| Pinecone | Store vectors and retrieve relevant content |
| Groq | Run the LLM used to generate answers |

## Project Structure

```text
taxxq/
├── core/
│   └── config.py
├── middlewares/
│   └── exception_handlers.py
├── modules/
│   └── embeddings.py
│   └── llm.py
│   └── load_vectorstore.py
│   └── pinecone_store.py
│   └── query_chain.py
├── logger.py
└── main.py

upload_docs/
.env
.gitignore
requirements.txt
README.md
```

## Getting Started

### Prerequisites

Before running TaxXQ, make sure you have:

- Python 3.10 or a compatible version supported by your dependencies
- A [Pinecone](https://www.pinecone.io/) account and API key
- A Google AI API key for Gemini embeddings
- A [Groq](https://console.groq.com/) account and API key

### 1. Clone the repository

```bash
git clone <repository-url>
cd taxxq
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Otherwise, install the packages used by the current implementation:

```bash
pip install fastapi uvicorn python-multipart pinecone \
  langchain-core langchain-community langchain-text-splitters \
  langchain-pinecone langchain-groq langchain-google-genai pypdf
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
PINECONE_API_KEY=your_pinecone_api_key
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
```

Make sure `taxxq/core/config.py` loads these variables and maps them to the settings used by the application. Use a Groq model ID currently supported by your account.

**Important:** Never commit API keys, `.env` files, or other secrets to GitHub.

### 5. Configure Pinecone

The application uses a Pinecone index named `taxxq`.

Before ingesting documents, verify that:

- The index exists in the correct region.
- Its vector dimension matches the output dimension of your embedding model.
- Document ingestion and query retrieval use the same embedding model and configuration.

If you change the embedding model or vector dimension, you may need to create a new index and re-index your documents.

### 6. Run the application

```bash
uv run fastapi dev src/taxxq/main.py
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```
