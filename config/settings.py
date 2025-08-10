import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "rag-index")
PINECONE_EMBED_MODEL = os.getenv("PINECONE_EMBED_MODEL", "all-mpnet-base-v2")
