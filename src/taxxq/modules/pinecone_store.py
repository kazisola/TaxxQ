from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from taxxq.core.config import settings
from taxxq.modules.embeddings import EMBEDDING_DIMENSION, get_embeddings

PINECONE_INDEX_NAME = "taxxq"
PINECONE_REGION = "us-east-1"

def get_pinecone():
    return Pinecone(
        api_key=settings.pinecone_api_key.get_secret_value()
    )

def ensure_pinecone():
    pc = get_pinecone()

    existing_indexes = pc.list_indexes().names()

    if PINECONE_INDEX_NAME not in existing_indexes:
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_REGION
            )
        )
    return pc

def get_vector_store():
    pc = ensure_pinecone()
    embeddings = get_embeddings()

    return PineconeVectorStore(
        pinecone_api_key=settings.pinecone_api_key.get_secret_value(),
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings
    )

def get_retriever():
    vector_store = get_vector_store()
    return vector_store.as_retriever(
        search_kwargs={"k": 4}
    )