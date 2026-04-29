import pytest
from datetime import date
from django.urls import reverse
from accounts.tests.factories import DoctorFactory, PatientFactory
from doctorsapp.models import DoctorAvailabilityModel


@pytest.mark.django_db
def test_patient_can_book_appointment(api_client):
    doctor_user = DoctorFactory()
    patient_user = PatientFactory()

    # IMPORTANT: availability add করতে হবে
    DoctorAvailabilityModel.objects.create(
    doctor=doctor_user.doctor_profile,
    day="Tuesday",
    start_time="09:00:00",
    end_time="17:00:00",
    is_active=True
)

    api_client.force_authenticate(user=patient_user)

    url = reverse("appointment-list")

    data = {
    "doctor": doctor_user.doctor_profile.id,
    "patient": patient_user.patient_profile.id,
    "date": "2030-01-01",  # 👉 এই date = Tuesday
    "time": "10:00:00",
    "reason_for_visit": "Fever"
}

    response = api_client.post(url, data)
    print(response.data)


    assert response.status_code == 201
