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