from django.db import models
from accounts.models import DoctorProfileModel, PatientProfileModel


class ReviewModel(models.Model):
    patient = models.ForeignKey(PatientProfileModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfileModel, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"{self.rating} - {self.doctor.user.email}"