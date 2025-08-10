import google.generativeai as genai
from config.settings import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

PROMPT_TEMPLATE = """
You are a helpful assistant. Use ONLY the provided CONTEXT to answer the QUESTION.
If you don't know the answer from the context, say "I don't know based on the provided documents."

CONTEXT:
{context}

QUESTION:
{question}

INSTRUCTIONS:
- Answer concisely (max 5 sentences)
- Add citations in format [source:filename | page:X]
"""

def answer_with_context(question, context_chunks):
    context_text = ""
    for chunk in context_chunks:
        src = chunk.metadata.get("source", "unknown")
        page = chunk.metadata.get("page", "N/A")
        context_text += f"[source:{src} | page:{page}]\n{chunk.page_content}\n\n"

    prompt = PROMPT_TEMPLATE.format(context=context_text, question=question)

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)
    return response.text
