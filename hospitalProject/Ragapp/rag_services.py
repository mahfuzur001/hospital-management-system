import faiss
import numpy as np
import google.generativeai as genai
from django.conf import settings
from sentence_transformers import SentenceTransformer
from .models import DoctorEmbeddingModel

# ১. Settings Check: আপনার settings.py ফাইলে GOOGLE_API_KEY সেট করা আছে কিনা নিশ্চিত করুন।
# ২. Initial Data: আপনার ডাটাবেজে কিছু ডাটা ঢোকানোর পর প্রথমেই একবার RAGService.generate_embeddings_for_all_doctors() কল করতে হবে (যেমন: Django Shell থেকে)। তা না হলে FAISS কোনো ডাটা পাবে না।


# ১. মডেল লোড করা (সার্ভার স্টার্ট হওয়ার সময় একবার লোড হবে)
# এটি টেক্সটকে ভেক্টরে রূপান্তর করবে
embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# ২. Gemini API কনফিগারেশন
genai.configure(api_key='AIzaSyCooRymYmAMUnWEzHTAJTe7tSw9SE5jgYA')

class RAGService:
    
    @staticmethod
    def generate_embeddings_for_all_doctors():
        """
        ডাটাবেজের সব 'content' থেকে ভেক্টর তৈরি করে ডাটাবেজেই সেভ করবে।
        """
        doctors_embeddings = DoctorEmbeddingModel.objects.filter(is_active=True)
        
        for item in doctors_embeddings:
            if item.content:
                # টেক্সট থেকে ভেক্টর জেনারেট করা
                vector = embedding_model.encode(item.content).tolist()
                item.embedding_vector = vector
                item.save()
        
        return "All embeddings updated successfully!"

    @staticmethod
    def build_faiss_index():
        """
        ডাটাবেজে সেভ করা ভেক্টরগুলো দিয়ে FAISS ইনডেক্স মেমোরিতে তৈরি করবে।
        """
        items = DoctorEmbeddingModel.objects.filter(
            is_active=True
        ).exclude(embedding_vector__isnull=True)
        
        if not items.exists():
            return None, []

        # ভেক্টরগুলোকে numpy array তে রূপান্তর (FAISS float32 সাপোর্ট করে)
        vectors = np.array([item.embedding_vector for item in items]).astype('float32')
        # ভেক্টরের সিরিয়াল অনুযায়ী ডাক্তারদের আইডি স্টোর করা
        doctor_ids = [item.doctor.id for item in items] 

        # FAISS ইনডেক্স তৈরি
        dimension = vectors.shape[1] # MiniLM এর ক্ষেত্রে এটি ৩৮৪
        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)
        
        return index, doctor_ids

    @staticmethod
    def ask_ai(user_query):
        """
        ইউজারের প্রশ্নের ভিত্তিতে সবচেয়ে উপযুক্ত ডাক্তার খুঁজে বের করে AI উত্তর দিবে।
        """
        # ১. ইনডেক্স এবং আইডি লিস্ট তৈরি করা
        index, doctor_ids = RAGService.build_faiss_index()
        
        if index is None:
            return "No doctor data found in the system."
        
        # ২. ইউজারের প্রশ্নকে ভেক্টরে রূপান্তর
        query_vector = embedding_model.encode([user_query]).astype('float32')
        
        # ৩. FAISS এ সার্চ করা (সবচেয়ে কাছের ৩ জন ডাক্তার)
        # D = Distance, I = Index
        D, I = index.search(query_vector, k=3)
        
        relevant_docs = []
        for i in I[0]:
            if i != -1: # -1 মানে কোনো ম্যাচ পাওয়া যায়নি
                doc_id = doctor_ids[i]
                try:
                    # খুঁজে পাওয়া ডাক্তারের কনটেন্ট নিয়ে আসা
                    doc_data = DoctorEmbeddingModel.objects.get(doctor_id=doc_id)
                    relevant_docs.append(doc_data.content)
                except DoctorEmbeddingModel.DoesNotExist:
                    continue

        # ৪. যদি কোনো উপযুক্ত ডাটা না পাওয়া যায়
        if not relevant_docs:
            return "Sorry, I couldn't find any suitable doctors for your query."

        # ৫. Gemini এর জন্য কনটেক্সট এবং প্রম্পট সাজানো
        context = "\n\n---\n\n".join(relevant_docs)
        prompt = f"""
        You are an intelligent Medical Assistant. Use the provided "Doctor Context" to answer the user's question accurately.
        If the answer is not in the context, politely inform the user.
        Always mention the doctor's name if you recommend someone.

        Doctor Context:
        {context}
        
        User Question: {user_query}
        
        Assistant Response:
        """

        # ৬. Gemini দিয়ে রেসপন্স জেনারেট করা
        gemini = genai.GenerativeModel('gemini-pro')
        response = gemini.generate_content(prompt)
        
        return response.text