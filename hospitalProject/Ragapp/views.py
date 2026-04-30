from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .rag_services import get_embedding_model, RAGService



class ChatWithDoctorAIView(APIView):

    def post(self, request):
        from .rag_services import RAGService  # 🔥 lazy import

        user_query = request.data.get('query')

        if not user_query:
            return Response(
                {"error": "Query is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ai_response = RAGService.ask_ai(user_query)

        return Response(
            {"response": ai_response},
            status=status.HTTP_200_OK
        )


class RebuildEmbeddingsView(APIView):
    """
    ডাটাবেজের সব ডাক্তারদের তথ্যের এমবেডিং নতুন করে তৈরি করার জন্য।
    """
    def post(self, request):
        try:
            message = RAGService.generate_embeddings_for_all_doctors()
            return Response({"message": message}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)