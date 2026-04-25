from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# ==========================================
# CUSTOM USER MODEL
# ==========================================
class UserModel(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
        ('STAFF', 'Staff'),
    )

    email = models.EmailField(unique=True) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_verified = models.BooleanField(default=False)
    address = models.TextField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

# ==========================================
# PROFILE MODELS
# ==========================================
class AdminProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Admin Profile: {self.user.username}"

class DoctorProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='doctor_profile')
    speciality = models.CharField(max_length=255, blank=True, null=True)
    experience = models.IntegerField(default=0)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    hospital_name = models.CharField(max_length=255, blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Doctor Profile: {self.user.username}"

class PatientProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='patient_profile')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    blood_group = models.CharField(max_length=5, null=True, blank=True)
    medical_history = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Patient Profile: {self.user.username}"

class StaffProfileModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='staff_profile')
    department = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"Staff Profile: {self.user.username}"

# ==========================================
# SIGNALS (AUTO-CREATE PROFILE)
# ==========================================
@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    """
    ইউজার তৈরি হওয়ার সাথে সাথে তার রোল অনুযায়ী প্রোফাইল অবজেক্ট তৈরি করবে।
    """
    if created:
        if instance.role == 'ADMIN':
            AdminProfileModel.objects.create(user=instance)
        elif instance.role == 'DOCTOR':
            DoctorProfileModel.objects.create(user=instance)
        elif instance.role == 'PATIENT':
            PatientProfileModel.objects.create(user=instance)
        elif instance.role == 'STAFF':
            StaffProfileModel.objects.create(user=instance)