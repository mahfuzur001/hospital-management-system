import pytest
from django.urls import reverse
from accounts.tests.factories import UserFactory, AdminFactory


@pytest.mark.django_db
def test_admin_can_create_doctor(api_client):
    admin = AdminFactory()

    api_client.force_authenticate(user=admin)

    url = reverse('admin-create-doctor')

    data = {
        "username": "doc1",
        "email": "doc@gmail.com",
        "password": "password123",
        "speciality": "Cardiology",
        "experience": 5,
        "qualification": "MBBS",
        "hospital_name": "ABC",
        "consultation_fee": "500"
    }

    response = api_client.post(url, data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_patient_cannot_create_doctor(api_client):
    user = UserFactory(role="PATIENT")

    api_client.force_authenticate(user=user)

    url = reverse('admin-create-doctor')

    response = api_client.post(url, {})

    # এখন ঠিক permission কাজ করলে 403 আসবে
    assert response.status_code == 403
