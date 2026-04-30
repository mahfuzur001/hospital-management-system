import pytest
from Ragapp.serializers import DoctorEmbeddingSerializer
from Ragapp.tests.factories import DoctorEmbeddingFactory


@pytest.mark.django_db
def test_embedding_serializer():
    obj = DoctorEmbeddingFactory()

    serializer = DoctorEmbeddingSerializer(obj)

    data = serializer.data

    assert "doctor_name" in data
    assert "doctor_email" in data
    assert data["content"] == obj.content