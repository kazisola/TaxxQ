from langchain_google_genai import GoogleGenerativeAIEmbeddings

EMBEDDING_MODEL = "gemeni-embedding-001"
EMBEDDING_DIMENSION = 768

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        output_dimensionality=EMBEDDING_DIMENSION,
    )