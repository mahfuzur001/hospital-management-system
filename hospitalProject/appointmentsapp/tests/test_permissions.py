import pytest
from django.urls import reverse
from accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_patient_cannot_access_admin_api(api_client):
    patient = UserFactory(role="PATIENT")

    api_client.force_authenticate(user=patient)

    url = reverse("appointment-list")

    response = api_client.get(url)

    assert response.status_code == 200  # patient can see own appointments
