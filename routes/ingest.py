from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from utils.file_loader import load_document
from utils.text_splitter import split_documents
from services.vector_store import upsert_texts

ingest_bp = Blueprint("ingest", __name__)
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@ingest_bp.route("/ingest", methods=["POST"])
def ingest_document():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Invalid file type"}), 400

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Extract text
        docs = load_document(filepath)
        chunks = split_documents(docs)

        # Metadata
        metadata = {
            "source": filepath,
            "filename": filename
        }

        # Store in Pinecone
        result = upsert_texts(chunks, metadata)

        return jsonify({
            "message": "Document ingested successfully",
            "details": result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
