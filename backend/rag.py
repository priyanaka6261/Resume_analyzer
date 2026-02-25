# ================================
# AI Resume Analyzer - RAG Module
# Uses Hugging Face DistilGPT2 + FAISS
# ================================

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import pipeline

# -------------------------------
# Load embedding model (Hugging Face)
# -------------------------------
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# -------------------------------
# Load lightweight LLM (DistilGPT2)
# Suitable for 4GB RAM systems
# -------------------------------
generator = pipeline("text-generation", model="distilgpt2")

# -------------------------------
# Vector Store Class
# -------------------------------


class VectorStore:
    def __init__(self):
        self.text_chunks = []
        self.index = faiss.IndexFlatL2(384)

    # Add text chunks to FAISS index
    def add_texts(self, texts):
        embeddings = embedding_model.encode(texts)
        self.index.add(np.array(embeddings))
        self.text_chunks.extend(texts)

    # Search similar chunks
    def search(self, query, k=4):
        if len(self.text_chunks) == 0:
            return ["No resume uploaded yet."]
        query_embedding = embedding_model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), k)
        return [self.text_chunks[i] for i in indices[0]]


# Global vector store instance
vector_store = VectorStore()

# -------------------------------
# LLM Response Generator
# -------------------------------


def generate_llm_response(prompt):
    result = generator(prompt, max_length=120, num_return_sequences=1)
    return result[0]["generated_text"]

# -------------------------------
# Main Answer Function
# -------------------------------


def generate_answer(query):
    # Retrieve relevant context
    context = " ".join(vector_store.search(query))

    # Prompt for LLM
    prompt = f"""
You must answer ONLY using the context.

If answer not found say "Not found".

Context:
{context}

Question:
{query}

Answer:
"""

    return generate_llm_response(prompt)
