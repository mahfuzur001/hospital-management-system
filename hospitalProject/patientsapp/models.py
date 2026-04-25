import os
from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import PatientProfileModel, DoctorProfileModel

# ফাইল আপলোডের পাথ নির্ধারণ (ইন্ডাস্ট্রি স্ট্যান্ডার্ড)
def patient_directory_path(instance, filename):
    # ফাইলটি মিডিয়া ফোল্ডারে patients/patient_id/records/filename হিসেবে সেভ হবে
    return f'patients/{instance.patient.id}/records/{filename}'

class MedicalRecordModel(models.Model):
    RECORD_TYPES = (
        ('GENERAL', 'General Checkup'),
        ('REPORT', 'Lab Report'),
        ('PRESCRIPTION', 'Prescription'),
        ('SURGERY', 'Surgery Record'),
        ('IMMUNIZATION', 'Immunization'),
    )

    patient = models.ForeignKey(
        PatientProfileModel, 
        on_delete=models.CASCADE, 
        related_name='medical_records'
    )
    # কোন ডাক্তার রেকর্ডটি যোগ করেছেন (ঐচ্ছিক হতে পারে যদি পেশেন্ট নিজে রিপোর্ট আপলোড করে)
    added_by = models.ForeignKey(
        DoctorProfileModel, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='added_records'
    )
    
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES, default='GENERAL')
    title = models.CharField(max_length=255, help_text="রেকর্ডের একটি সংক্ষিপ্ত শিরোনাম (যেমন: Blood Test Report)")
    description = models.TextField(blank=True, null=True)
    
    # ফাইল আপলোড অপশন (পিডিএফ বা ইমেজ)
    document = models.FileField(
        upload_to=patient_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        null=True, 
        blank=True,
        help_text="ডকুমেন্টের স্ক্যান কপি আপলোড করুন (PDF, JPG, PNG)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Medical Record"
        verbose_name_plural = "Medical Records"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.patient.user.get_full_name()}"

    @property
    def file_extension(self):
        if self.document:
            extension = os.path.splitext(self.document.name)[1]
            return extension.lower()
        return None