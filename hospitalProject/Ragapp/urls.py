from django.urls import path
from .views import ChatWithDoctorAIView, RebuildEmbeddingsView

urlpatterns = [
    path('chat/', ChatWithDoctorAIView.as_view(), name='chat-with-ai'),
    path('rebuild-embeddings/', RebuildEmbeddingsView.as_view(), name='rebuild-embeddings'),
]