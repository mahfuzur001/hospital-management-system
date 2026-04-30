import os
import sys
import faiss
import numpy as np
import google.generativeai as genai
from django.conf import settings
from .models import DoctorEmbeddingModel


_embedding_model = None
_gemini_model = None


def is_testing():
    return (
        "pytest" in sys.modules
        or os.environ.get("PYTEST_CURRENT_TEST")
        or os.environ.get("TESTING") == "1"
    )


def get_embedding_model():
    global _embedding_model

    if is_testing():
        return None

    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    return _embedding_model


def get_gemini_model():
    global _gemini_model

    if is_testing():
        return None

    if _gemini_model is None:
        api_key = getattr(settings, "GOOGLE_API_KEY", None)

        if not api_key:
            raise ValueError("GOOGLE_API_KEY missing")

        genai.configure(api_key=api_key)
        _gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    return _gemini_model


class RAGService:

    @staticmethod
    def generate_embeddings_for_all_doctors():
        model = get_embedding_model()

        if model is None:
            return "Skipped in test mode"

        doctors = DoctorEmbeddingModel.objects.filter(is_active=True)

        count = 0

        for item in doctors:
            vector = model.encode(item.content)
            item.embedding_vector = vector.tolist()
            item.save(update_fields=["embedding_vector"])
            count += 1

        return f"{count} embeddings updated"

    @staticmethod
    def build_faiss_index():
        items = list(
            DoctorEmbeddingModel.objects.filter(
                is_active=True,
                embedding_vector__isnull=False
            )
        )

        if not items:
            return None, []

        vectors = np.array([i.embedding_vector for i in items], dtype="float32")

        index = faiss.IndexFlatL2(vectors.shape[1])
        index.add(vectors)

        return index, items

    @staticmethod
    def retrieve_relevant_doctors(query, top_k=3):
        model = get_embedding_model()

        if model is None:
            return []

        index, items = RAGService.build_faiss_index()

        if index is None:
            return []

        q_vec = model.encode([query]).astype("float32")

        _, indices = index.search(q_vec, top_k)

        results = []

        for i in indices[0]:
            if i == -1:
                continue
            results.append(items[i].content)

        return results

    @staticmethod
    def ask_ai(query):
        docs = RAGService.retrieve_relevant_doctors(query)

        if not docs:
            return "No relevant doctors found."

        context = "\n\n---\n\n".join(docs)

        prompt = f"""
You are a medical assistant.

Context:
{context}

Question:
{query}

Answer:
"""

        gemini = get_gemini_model()

        if gemini is None:
            return "Skipped in test mode"

        response = gemini.generate_content(prompt)
        return response.text