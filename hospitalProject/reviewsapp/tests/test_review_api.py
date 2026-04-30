import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_patient_can_create_review(api_client, patient, doctor, completed_appointment):

    api_client.force_authenticate(user=patient)

    url = reverse("review-list-create")

    data = {
        "doctor": doctor.doctor_profile.id,
        "rating": 5,
        "comment": "Excellent doctor"
    }

    response = api_client.post(url, data)

    assert response.status_code == 201
    assert response.data["rating"] == 5


@pytest.mark.django_db
def test_patient_can_view_reviews(api_client, patient, doctor):

    api_client.force_authenticate(user=patient)

    url = reverse("review-list-create")

    response = api_client.get(url)

    assert response.status_code == 200
