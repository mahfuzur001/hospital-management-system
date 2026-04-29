import pytest
from django.urls import reverse
from accounts.tests.factories import PatientFactory


# =========================
# PATIENT CANNOT CREATE RECORD
# =========================
@pytest.mark.django_db
def test_patient_cannot_create_record(api_client):
    patient = PatientFactory()

    api_client.force_authenticate(user=patient)

    url = reverse("medical-record-list")

    data = {
        "record_type": "REPORT",
        "title": "Test Report"
    }

    response = api_client.post(url, data)

    assert response.status_code in [403, 400]
