from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from taxxq.modules.pinecone_store import get_vector_store

UPLOAD_DIR = Path("./upload_docs")
UPLOAD_DIR.mkdir(exist_ok=True)

def load_vectorstore(uploaded_files):
    vector_store = get_vector_store()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )

    total_chunks = 0

    for file in uploaded_files:
        # Save the uploaded files
        if not file.filename:
            raise ValueError("Uploaded file must have a filename")
        if not file.filename.lowercase().endswith(".pdf"):
            raise TypeError("Only PDF files are supported")

        file_path = UPLOAD_DIR / Path(file.filename).name

        with open(file_path, "wb") as f:
            # Read the uploaded file in blocks of up to 1 MiB
            while True:
                chunk = file.file.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)

        print(f"Saved {file_path}")

        # Convert file into documents and create chunks
        loader = PyPDFLoader(str(file_path))
        documents = loader.load()

        chunks = splitter.split_documents(documents)

        # Add metadata to chunks
        for chunk in chunks:
            chunk.metadata["source"] = file_path.name

        # Documents > Embeddings > Pinecone
        vector_store.add_documents(documents=chunks)

        total_chunks += len(chunks)

        print(f"Added {len(chunks)} chunks from {file_path.name}")

        return total_chunks