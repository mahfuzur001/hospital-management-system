import pytest
from django.urls import reverse
from accounts.tests.factories import AdminFactory


@pytest.mark.django_db
def test_doctor_cannot_create_review(api_client, doctor):

    api_client.force_authenticate(user=doctor)

    url = reverse("review-list-create")

    data = {
        "doctor": doctor.doctor_profile.id,
        "rating": 4,
        "comment": "Nice"
    }

    response = api_client.post(url, data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_cannot_create_review(api_client):

    admin = AdminFactory()
    api_client.force_authenticate(user=admin)

    url = reverse("review-list-create")

    data = {
        "doctor": 1,
        "rating": 4,
        "comment": "Test"
    }

    response = api_client.post(url, data)

    assert response.status_code == 403
