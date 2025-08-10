
from sentence_transformers import SentenceTransformer
from config import settings

# You can change the model name if you want a different embedding model
EMBEDDING_MODEL = getattr(settings, 'PINECONE_EMBED_MODEL', 'all-mpnet-base-v2')
_model = SentenceTransformer(EMBEDDING_MODEL)

def get_embeddings(texts):
    """Generate embeddings for a list of text chunks using sentence-transformers."""
    return _model.encode(texts, show_progress_bar=False).tolist()
