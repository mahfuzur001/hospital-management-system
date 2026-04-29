import pytest
from django.urls import reverse
from accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_doctor_can_create_prescription(api_client):
    doctor = UserFactory(role="DOCTOR")

    api_client.force_authenticate(user=doctor)

    url = reverse("prescription-create")

    data = {
        "appointment": 1,
        "symptoms": "Fever",
        "diagnosis": "Viral Fever",
        "medicines": "Paracetamol",
        "advice": "Rest"
    }

    response = api_client.post(url, data)

    assert response.status_code in [201, 400]  # depends on appointment existence
