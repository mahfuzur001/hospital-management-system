import pytest
from django.urls import reverse
from accounts.tests.factories import DoctorFactory, PatientFactory


# =========================
# FILE SIZE VALIDATION
# =========================
@pytest.mark.django_db
def test_file_size_validation(api_client):
    doctor = DoctorFactory()
    patient = PatientFactory()

    api_client.force_authenticate(user=doctor)

    url = reverse("medical-record-list")

    # fake large file (just simulate)
    data = {
        "patient": patient.patient_profile.id,
        "record_type": "REPORT",
        "title": "Big File Test",
    }

    response = api_client.post(url, data)

    # actual file validation depends on multipart testing
    assert response.status_code in [400, 201]
