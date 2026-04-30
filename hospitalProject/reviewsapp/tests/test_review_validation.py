import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_review_without_completed_appointment_fails(api_client, patient, doctor):

    api_client.force_authenticate(user=patient)

    url = reverse("review-list-create")

    data = {
        "doctor": doctor.doctor_profile.id,
        "rating": 5,
        "comment": "Good"
    }

    response = api_client.post(url, data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_rating_validation(api_client, patient, doctor, completed_appointment):

    api_client.force_authenticate(user=patient)

    url = reverse("review-list-create")

    data = {
        "doctor": doctor.doctor_profile.id,
        "rating": 10,   # invalid
        "comment": "Bad test"
    }

    response = api_client.post(url, data)

    assert response.status_code == 400
