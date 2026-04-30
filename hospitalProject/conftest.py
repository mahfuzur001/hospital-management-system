import pytest
from rest_framework.test import APIClient

from accounts.tests.factories import PatientFactory, DoctorFactory
from appointmentsapp.models import AppointmentModel

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()






@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(db):
    from accounts.tests.factories import PatientFactory

    user = PatientFactory()
    client = APIClient()
    client.force_authenticate(user=user)
    return client



@pytest.fixture
def doctor(db):
    return DoctorFactory()


@pytest.fixture
def patient(db):
    return PatientFactory()


@pytest.fixture
def completed_appointment(db, patient, doctor):
    return AppointmentModel.objects.create(
        patient=patient.patient_profile,
        doctor=doctor.doctor_profile,
        date="2025-04-01",
        time="10:00:00",
        status="COMPLETED"
    )
    
    
import pytest

@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass