from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from taxxq.middlewares.exception_handlers import catch_exception_middleware

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

# Middleware Exceptions
app.middleware("http")(catch_exception_middleware)