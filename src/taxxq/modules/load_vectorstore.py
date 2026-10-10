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

    # Save the uploaded files

    for file in uploaded_files:
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