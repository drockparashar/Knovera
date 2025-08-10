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

        # Format output
        sources = [
            {
                "score": match["score"],
                "source": match["metadata"].get("source"),
                "page": match["metadata"].get("page", None),
                "chunk_id": match["metadata"].get("chunk_id"),
                "text": match["metadata"].get("text")
            }
            for match in results["matches"]
        ]

        return jsonify({
            "answer": "TODO: Connect LLM for answer generation",
            "sources": sources
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
