from django.db import models
from accounts.models import DoctorProfileModel


class DoctorAvailabilityModel(models.Model):
    doctor = models.ForeignKey(DoctorProfileModel, on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.user.email} - {self.day}"