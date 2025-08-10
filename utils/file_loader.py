import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
import docx2txt

def load_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        docs = loader.load()
    elif ext == ".docx":
        text = docx2txt.process(file_path)
        docs = [{"page_content": text, "metadata": {"source": file_path}}]
    elif ext == ".txt":
        loader = TextLoader(file_path)
        docs = loader.load()
    else:
        raise ValueError("Unsupported file type")

    return docs
