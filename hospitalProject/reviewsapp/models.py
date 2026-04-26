from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import DoctorProfileModel, PatientProfileModel


class ReviewModel(models.Model):
    patient = models.ForeignKey(
        PatientProfileModel,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    doctor = models.ForeignKey(
        DoctorProfileModel,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        help_text="Rating must be between 1 and 5"
    )

    comment = models.TextField(
        help_text="Patient feedback about the doctor"
    )

    # 🔥 AI / RAG ready field
    is_verified = models.BooleanField(
        default=False,
        help_text="Only verified reviews will be used in AI recommendation"
    )

    # 📊 Industry standard timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

        # 🚨 One patient → one review per doctor
        unique_together = ('patient', 'doctor')

        ordering = ['-created_at']

    def __str__(self):
        return f"{self.patient.user.email} → {self.doctor.user.email} ({self.rating})"