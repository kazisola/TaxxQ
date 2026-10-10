from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from taxxq.modules.pinecone_store import get_vector_store

UPLOAD_DIR = Path("./upload_docs")
UPLOAD_DIR.mkdir(exist_ok=True)

def load_vectorstore(uploaded_files):
    vector_store = get_vector_store()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    