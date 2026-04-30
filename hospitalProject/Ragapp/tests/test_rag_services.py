import pytest
from unittest.mock import patch
from Ragapp.rag_services import RAGService


@patch("Ragapp.rag_services.RAGService.retrieve_relevant_doctors")
@patch("Ragapp.rag_services.get_gemini_model")
@pytest.mark.django_db
def test_ask_ai_mocked(mock_gemini, mock_retrieve):

    # ✅ FAISS/RAG mock
    mock_retrieve.return_value = ["Heart specialist doctor"]

    # ✅ Gemini mock
    mock_model = mock_gemini.return_value
    mock_model.generate_content.return_value.text = "Mock response"

    # ❗ CALL REAL FUNCTION
    response = RAGService.ask_ai("I need doctor")

    # ✅ ASSERT
    assert response == "Mock response"