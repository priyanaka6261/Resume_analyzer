from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')


class VectorStore:
    def __init__(self):
        self.text_chunks = []
        self.index = faiss.IndexFlatL2(384)

    def add_texts(self, texts):
        embeddings = model.encode(texts)
        self.index.add(np.array(embeddings))
        self.text_chunks.extend(texts)

    def search(self, query, k=4):
        if len(self.text_chunks) == 0:
            return ["No resume uploaded yet."]
        query_embedding = model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding), k)
        return [self.text_chunks[i] for i in indices[0]]


vector_store = VectorStore()

# Answer generator


def generate_answer(query):
    context = " ".join(vector_store.search(query))
    query_lower = query.lower()

    if "summary" in query_lower:
        return f"Professional Summary:\n{context[:400]}..."

    elif "skill" in query_lower:
        return f"Key Skills:\n{context[:400]}..."

    elif "education" in query_lower:
        return f"Education Details:\n{context[:400]}..."

    elif "experience" in query_lower:
        return f"Experience:\n{context[:400]}..."

    elif "strength" in query_lower:
        return "Strengths include strong technical background and project experience."

    elif "weakness" in query_lower:
        return "Areas to improve include adding certifications and measurable achievements."

    else:
        return f"Relevant Information:\n{context[:400]}..."
