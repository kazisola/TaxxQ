from langchain_google_genai import GoogleGenerativeAIEmbeddings
from taxxq.core.config import settings

EMBEDDING_MODEL = "gemini-embedding-001"
EMBEDDING_DIMENSION = 768

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        api_key=settings.google_api_key,
        model=EMBEDDING_MODEL,
        output_dimensionality=EMBEDDING_DIMENSION,
    )