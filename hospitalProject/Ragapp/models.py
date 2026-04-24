from django.db import models
from accounts.models import DoctorProfileModel


class DoctorEmbeddingModel(models.Model):
    doctor = models.ForeignKey(DoctorProfileModel, on_delete=models.CASCADE)
    content = models.TextField()  # text তৈরি করে embedding হবে
    embedding_vector = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.doctor.user.email