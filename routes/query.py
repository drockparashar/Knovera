from flask import Blueprint, request, jsonify
from services.vector_store import query_text

query_bp = Blueprint("query", __name__)

@query_bp.route("/query", methods=["POST"])
def query_documents():
    try:
        data = request.get_json()
        query = data.get("query")
        top_k = data.get("top_k", 5)

        if not query:
            return jsonify({"error": "Query text is required"}), 400

        # Retrieve results from Pinecone
        results = query_text(query, top_k)
        # Debug: print raw Pinecone results
        print("Pinecone raw results:", results)

        # Format output and prepare context for LLM
        sources = []
        context_chunks = []
        for match in results["matches"]:
            sources.append({
                "score": match["score"],
                "source": match["metadata"].get("source"),
                "page": match["metadata"].get("page", None),
                "chunk_id": match["metadata"].get("chunk_id"),
                "text": match["metadata"].get("text")
            })
            # Prepare a chunk-like object for LLM
            class Chunk:
                def __init__(self, metadata, page_content):
                    self.metadata = metadata
                    self.page_content = page_content
            context_chunks.append(
                Chunk(match["metadata"], match["metadata"].get("text", ""))
            )

        # Import and use the LLM answer generator
        from services.llm import answer_with_context
        answer = answer_with_context(query, context_chunks)

        return jsonify({
            "answer": answer,
            "sources": sources
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
