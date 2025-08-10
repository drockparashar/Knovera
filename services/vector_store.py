
from pinecone import Pinecone, ServerlessSpec
import uuid
from config import settings
from services.embeddings import get_embeddings

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

# Optional: create index if it doesn't exist
if settings.PINECONE_INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=settings.PINECONE_INDEX_NAME,
        dimension=768,  # matches all-mpnet-base-v2
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")  # adjust as needed
    )
index = pc.Index(settings.PINECONE_INDEX_NAME)

def upsert_texts(texts, metadata):
    # Extract text content if input is a list of chunk objects
    if texts and hasattr(texts[0], 'page_content'):
        text_list = [chunk.page_content for chunk in texts]
    else:
        text_list = texts

    vectors = []
    embeddings = get_embeddings(text_list)

    for i, emb in enumerate(embeddings):
        vectors.append({
            "id": f"{metadata.get('filename', 'doc')}-{uuid.uuid4()}",
            "values": emb,
            "metadata": {
                **metadata,
                "chunk_id": i,
                "text": text_list[i]
            }
        })

    # Use namespace if provided in metadata, else default
    namespace = metadata.get("namespace", "default")
    index.upsert(vectors, namespace=namespace)
    return {"status": "success", "count": len(vectors), "namespace": namespace}

def query_text(query, top_k=5):
    query_embedding = get_embeddings([query])[0]
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    return results
