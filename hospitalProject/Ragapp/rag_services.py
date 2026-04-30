# Ragapp/rag_services.py
import os
import faiss
import numpy as np
import google.generativeai as genai

from django.conf import settings
from .models import DoctorEmbeddingModel


# =========================================================
# 🔒 GLOBAL CACHE
# =========================================================
_embedding_model = None
_gemini_model = None


# =========================================================
# 🧪 TEST CHECK (SAFE WAY)
# =========================================================
def is_testing():
    return "pytest" in sys.modules or os.environ.get("PYTEST_CURRENT_TEST")


# =========================================================
# 🔥 EMBEDDING MODEL (LAZY LOAD)
# =========================================================
def get_embedding_model():
    global _embedding_model

    if is_testing():
        return None

    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    return _embedding_model


# =========================================================
# 🤖 GEMINI MODEL (LAZY LOAD)
# =========================================================
def get_gemini_model():
    global _gemini_model

    if is_testing():
        return None

    if _gemini_model is None:
        api_key = getattr(settings, "GOOGLE_API_KEY", None)

        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in settings.py")

        genai.configure(api_key=api_key)

        # 🔥 stable model
        _gemini_model = genai.GenerativeModel("gemini-1.5-flash")

    return _gemini_model


# =========================================================
# 🧠 RAG SERVICE
# =========================================================
class RAGService:

    @staticmethod
    def generate_embeddings_for_all_doctors():
        model = get_embedding_model()

        if model is None:
            return "Skipped in test mode"

        doctors = DoctorEmbeddingModel.objects.filter(is_active=True)

        count = 0

        for item in doctors:
            if item.content:
                vector = model.encode(item.content)

                item.embedding_vector = vector.tolist()
                item.save(update_fields=["embedding_vector"])

                count += 1

        return f"{count} embeddings updated"

    # =====================================================
    # FAISS INDEX
    # =====================================================
    @staticmethod
    def build_faiss_index():
        items = DoctorEmbeddingModel.objects.filter(
            is_active=True,
            embedding_vector__isnull=False
        )

        if not items.exists():
            return None, []

        vectors = np.array(
            [item.embedding_vector for item in items],
            dtype="float32"
        )

        doctor_ids = [item.doctor.id for item in items]

        dimension = vectors.shape[1]

        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)

        return index, doctor_ids

    # =====================================================
    # RETRIEVE
    # =====================================================
    @staticmethod
    def retrieve_relevant_doctors(user_query, top_k=3):
        model = get_embedding_model()

        if model is None:
            return []

        index, doctor_ids = RAGService.build_faiss_index()

        if index is None:
            return []

        query_vector = model.encode([user_query]).astype("float32")

        _, indices = index.search(query_vector, top_k)

        results = []

        for i in indices[0]:
            if i == -1:
                continue

            try:
                doc = DoctorEmbeddingModel.objects.get(
                    doctor_id=doctor_ids[i]
                )

                results.append(doc.content)

            except DoctorEmbeddingModel.DoesNotExist:
                continue

        return results

    # =====================================================
    # MAIN AI FUNCTION
    # =====================================================
    @staticmethod
    def ask_ai(user_query):
        docs = RAGService.retrieve_relevant_doctors(user_query)

        if not docs:
            return "No relevant doctors found."

        context = "\n\n---\n\n".join(docs)

        prompt = f"""
You are a medical assistant.

Use ONLY this context:

{context}

Question:
{user_query}

Answer:
"""

        gemini = get_gemini_model()

        if gemini is None:
            return "Skipped in test mode"

        try:
            response = gemini.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"AI Error: {str(e)}"