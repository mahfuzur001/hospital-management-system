import pytest
from django.urls import reverse

from accounts.tests.factories import DoctorFactory, PatientFactory, AdminFactory
from doctorsapp.models import DoctorAvailabilityModel


# ==============================
# 1. OVERLAPPING SLOT TEST
# ==============================
@pytest.mark.django_db
def test_overlapping_time_slot_not_allowed(api_client):
    doctor = DoctorFactory()

    api_client.force_authenticate(user=doctor)

    url = reverse("availability-list")

    DoctorAvailabilityModel.objects.create(
        doctor=doctor.doctor_profile,
        day="Monday",
        start_time="09:00:00",
        end_time="12:00:00",
        is_active=True
    )

    data = {
        "day": "Monday",
        "start_time": "11:00:00",
        "end_time": "14:00:00",
        "is_active": True
    }

    response = api_client.post(url, data)

    print(response.data)

    assert response.status_code == 400


# ==============================
# 2. PATIENT CANNOT CREATE SLOT
# ==============================
@pytest.mark.django_db
def test_patient_cannot_create_availability(api_client):
    patient = PatientFactory()

    api_client.force_authenticate(user=patient)

    url = reverse("availability-list")

    data = {
        "day": "Monday",
        "start_time": "09:00:00",
        "end_time": "17:00:00",
        "is_active": True
    }

    response = api_client.post(url, data)

    print(response.data)

    assert response.status_code in [400, 403]


# ==============================
# 3. ADMIN CAN CREATE SLOT
# ==============================
@pytest.mark.django_db
def test_admin_can_create_availability(api_client):
    admin = AdminFactory()

    api_client.force_authenticate(user=admin)

    doctor = DoctorFactory()

    url = reverse("availability-list")

    data = {
        "doctor": doctor.doctor_profile.id,
        "day": "Tuesday",
        "start_time": "10:00:00",
        "end_time": "15:00:00",
        "is_active": True
    }

    response = api_client.post(url, data)

    print(response.data)

    assert response.status_code == 201
