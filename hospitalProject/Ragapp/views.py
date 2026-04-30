from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .rag_services import RAGService


class ChatWithDoctorAIView(APIView):

    def post(self, request):
        query = request.data.get("query")

        if not query:
            return Response(
                {"error": "Query is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = RAGService.ask_ai(query)

        return Response({"response": result})


class RebuildEmbeddingsView(APIView):

    def post(self, request):
        try:
            msg = RAGService.generate_embeddings_for_all_doctors()
            return Response({"message": msg})
        except Exception as e:
            return Response({"error": str(e)}, status=500)