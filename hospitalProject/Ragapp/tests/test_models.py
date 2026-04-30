import pytest
from Ragapp.tests.factories import DoctorEmbeddingFactory


@pytest.mark.django_db
def test_doctor_embedding_creation():
    obj = DoctorEmbeddingFactory()

    assert obj.id is not None
    assert obj.content is not None
    assert obj.is_active is True