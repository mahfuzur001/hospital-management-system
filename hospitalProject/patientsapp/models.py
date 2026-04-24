from django.db import models
from accounts.models import PatientProfileModel


class MedicalRecordModel(models.Model):
    patient = models.ForeignKey(PatientProfileModel, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)