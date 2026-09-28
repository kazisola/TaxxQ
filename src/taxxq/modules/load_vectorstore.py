import os
import time
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from tqdm import tqdm
from taxxq.core.config import settings

PINECONE_ENV = "us-east-1"
PINECONE_INDEX_NAME = "taxxq"

UPLOAD_DIR = "./upload_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Inititalize Pinecone
pinecone = Pinecone(api_key=settings.pinecone_api_key.get_secret_value())
spec = ServerlessSpec(
    cloud="aws",
    region=PINECONE_ENV
)

existing_indexes = [i["name"] for i in pinecone.list_indexes()]

if PINECONE_INDEX_NAME not in existing_indexes:
    pinecone.create_index(
        name=PINECONE_INDEX_NAME,
        dimension=1024,
        metric="cosine",
        spec=spec
    )

    while not pinecone.describe_index(PINECONE_INDEX_NAME).status["ready"]:
        time.sleep(1)

index = pinecone.Index(PINECONE_INDEX_NAME)


# Load, split, embed and upsert PDF docs content
def load_vectorstore(uploaded_files):
    embed_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    file_paths = []

    # 1. Upload docs
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR)/file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())

        file_paths.append(save_path)

    for file_path in file_paths:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        #  2. Split docs
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(documents)

        texts = [chunk.page_content for chunk in chunks]
        metadata = [chunk.metadata for chunk in chunks]
        ids = [f"{Path(file_path).stem}-{i}" for i in range(len(chunks))]

        # 3. Embed chunks
        print("Embedding...")
        embeddings = embed_model.embed_documents(texts)

        # 4. Upsert
        with tqdm(total=len(embeddings), desc="Upserting to Pinecone") as progress:
            vectors = [{ "id": vector_id, "values": embedding, "metadata": meta } for vector_id, embedding, meta in zip(ids, embeddings, metadata)]
            index.upsert(vectors=vectors)
            progress.update(len(embeddings))

        print(f"Upload completed for {file_path}")