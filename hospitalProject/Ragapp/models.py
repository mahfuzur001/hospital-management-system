from django.db import models
from accounts.models import DoctorProfileModel


class DoctorEmbeddingModel(models.Model):
    doctor = models.ForeignKey(
        DoctorProfileModel,
        on_delete=models.CASCADE,
        related_name='embeddings'
    )

    # 🧠 AI এর জন্য clean text
    content = models.TextField(
        help_text="Doctor profile + reviews combined text for embedding"
    )

    # 🔢 vector (store temporarily বা debug purpose)
    embedding_vector = models.JSONField(
        blank=True,
        null=True,
        help_text="Optional: store embedding vector (FAISS হলে না রাখলেও চলে)"
    )

    # 🔥 version control (important for re-embedding)
    embedding_model = models.CharField(
        max_length=100,
        default="sentence-transformers/all-MiniLM-L6-v2",
        help_text="Which embedding model was used"
    )

    # 📊 metadata (future filtering)
    metadata = models.JSONField(
        blank=True,
        null=True,
        help_text="Extra info like speciality, rating, experience"
    )

    # 🔄 tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 🔥 active flag (rebuild / soft delete)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Doctor Embedding"
        verbose_name_plural = "Doctor Embeddings"
        indexes = [
            models.Index(fields=['doctor']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.doctor.user.email} - Embedding"