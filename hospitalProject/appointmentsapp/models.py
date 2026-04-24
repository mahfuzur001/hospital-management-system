from django.db import models
from accounts.models import DoctorProfileModel, PatientProfileModel


class AppointmentModel(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )

    patient = models.ForeignKey(PatientProfileModel, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfileModel, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.patient.user.email} -> {self.doctor.user.email}"
    

class PrescriptionModel(models.Model):
    appointment = models.OneToOneField(AppointmentModel, on_delete=models.CASCADE)
    doctor_notes = models.TextField()
    medicines = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)