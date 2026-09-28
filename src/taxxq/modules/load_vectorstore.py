import os
import time
from pathlib import Path
from pinecone import Pinecone, ServerlessSpec
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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

    # 1. Upload
    for file in uploaded_files:
        save_path = Path(UPLOAD_DIR)/file.filename
        with open(save_path, "wb") as f:
            f.write(file.file.read())

        file_paths.append(save_path)