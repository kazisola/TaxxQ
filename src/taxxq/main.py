from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from taxxq.middlewares.exception_handlers import catch_exception_middleware
from taxxq.modules.load_vectorstore import load_vectorstore

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

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.post("documents")
def upload_docs(
    files: list[UploadFile] = File(...)
    ):
    counts = load_vectorstore(files)
    return {
        "message": "Documents indexed successfully",
        "counts": counts,
    }

# Middleware Exceptions
app.middleware("http")(catch_exception_middleware)