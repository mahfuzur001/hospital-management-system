import pytest
from django.urls import reverse
from accounts.tests.factories import PatientFactory, DoctorFactory, AdminFactory
from patientsapp.models import MedicalRecordModel


# =========================
# 1. PATIENT CAN SEE OWN RECORDS
# =========================
@pytest.mark.django_db
def test_patient_can_view_own_records(api_client):
    patient = PatientFactory()

    api_client.force_authenticate(user=patient)

    url = reverse("medical-record-list")

    response = api_client.get(url)

    assert response.status_code == 200


# =========================
# 2. ADMIN CAN VIEW ALL RECORDS
# =========================
@pytest.mark.django_db
def test_admin_can_view_all_records(api_client):
    admin = AdminFactory()

    api_client.force_authenticate(user=admin)

    url = reverse("medical-record-list")

    response = api_client.get(url)

    assert response.status_code == 200


# =========================
# 3. DOCTOR CAN CREATE RECORD
# =========================
@pytest.mark.django_db
def test_doctor_can_create_medical_record(api_client):
    doctor = DoctorFactory()
    patient = PatientFactory()

    api_client.force_authenticate(user=doctor)

    url = reverse("medical-record-list")

    data = {
        "patient": patient.patient_profile.id,
        "record_type": "REPORT",
        "title": "Blood Test",
        "description": "Normal report"
    }

    response = api_client.post(url, data)

    assert response.status_code == 201
