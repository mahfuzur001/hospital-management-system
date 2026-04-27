from django.urls import path
from .views import ChatWithDoctorAIView, RebuildEmbeddingsView

urlpatterns = [
    # ইউজার এই লিঙ্কে তার প্রশ্ন পাঠাবে
    # POST request: {"query": "I need a cardiologist for my father"}
    path('chat/', ChatWithDoctorAIView.as_view(), name='chat-with-ai'),

    # এটি শুধু অ্যাডমিন বা ডেভেলপার ব্যবহার করবে এমবেডিং আপডেট করতে
    # POST request (Empty)
    path('rebuild-embeddings/', RebuildEmbeddingsView.as_view(), name='rebuild-embeddings'),
]