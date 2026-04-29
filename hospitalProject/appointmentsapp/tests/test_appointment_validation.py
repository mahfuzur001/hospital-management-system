import pytest
from appointmentsapp.models import AppointmentModel


@pytest.mark.django_db
def test_unique_doctor_slot():
    AppointmentModel.objects.create(
        patient_id=1,
        doctor_id=1,
        date="2030-01-01",
        time="10:00:00"
    )

    with pytest.raises(Exception):
        AppointmentModel.objects.create(
            patient_id=2,
            doctor_id=1,
            date="2030-01-01",
            time="10:00:00"
        )
