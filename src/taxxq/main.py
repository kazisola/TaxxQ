from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from taxxq.middlewares.exception_handlers import catch_exception_middleware
from taxxq.modules.load_vectorstore import load_vectorstore
from taxxq.modules.llm import get_llm, get_prompt
from taxxq.modules.pinecone_store import get_retriever
from taxxq.modules.query_chain import query_chain
from pydantic import BaseModel

app = FastAPI(
        title="TaxxQ",
        description="AI-Powered US Tax Query"
    )

# CORS POLICY
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class QuestionRequest(BaseModel):
    question: str

retriever = get_retriever()
llm = get_llm()
prompt = get_prompt()

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("/documents")
def upload_docs(
    files: list[UploadFile] = File(...)
):
    counts = load_vectorstore(files)
    return {
        "message": "Documents indexed successfully",
        "counts": counts,
    }

@app.post("/ask")
def ask_question(request: QuestionRequest):
    return query_chain(
        retriever,
        llm,
        prompt,
        user_input=request.question,
    )

# Middleware Exceptions
app.middleware("http")(catch_exception_middleware)
