import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from Ragapp.tests.factories import DoctorEmbeddingFactory


@pytest.mark.django_db
def test_chat_api():
    client = APIClient()

    DoctorEmbeddingFactory()

    url = reverse("chat-with-ai")

    response = client.post(url, {"query": "heart doctor"})

    assert response.status_code == 200


@pytest.mark.django_db
def test_rebuild_embeddings_api():
    client = APIClient()

    url = reverse("rebuild-embeddings")

    response = client.post(url)

    assert response.status_code == 200