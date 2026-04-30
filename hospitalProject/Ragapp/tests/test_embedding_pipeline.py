import pytest
from Ragapp.tests.factories import DoctorEmbeddingFactory
from Ragapp.rag_services import RAGService


@pytest.mark.django_db
def test_generate_embeddings():
    DoctorEmbeddingFactory.create_batch(2)

    result = RAGService.generate_embeddings_for_all_doctors()

    assert "updated" in result or "Skipped" in result