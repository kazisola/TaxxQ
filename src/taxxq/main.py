from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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