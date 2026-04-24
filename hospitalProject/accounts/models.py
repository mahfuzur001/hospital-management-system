from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
        ('STAFF', 'Staff'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)
    address=models.TextField(blank=True, null=True)
    mobile_number=models.CharField(max_length=15, blank=True, null=True)

    

    def __str__(self):
        return self.username
    
class AdminProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Admin: {self.user.username}"
    
class DoctorProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=255)
    experience = models.IntegerField(help_text="Years of experience")
    qualification = models.CharField(max_length=255)
    hospital_name = models.CharField(max_length=255)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"Doctor: {self.user.username}"
    
class PatientProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Patient: {self.user.username}"
    
class StaffProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    
    def __str__(self):
        return f"Staff: {self.user.username}"