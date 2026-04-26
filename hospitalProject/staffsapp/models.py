from django.db import models
from accounts.models import StaffProfileModel, UserModel


class TaskModel(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
        ('CANCELLED', 'Cancelled'),
    )

    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )

    # 👤 কে task পেয়েছে
    staff = models.ForeignKey(
        StaffProfileModel,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    # 👨‍💼 কে assign করেছে (admin/doctor)
    assigned_by = models.ForeignKey(
        UserModel,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assigned_tasks'
    )

    # 📌 task details
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # 🔥 workflow
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )
    
    category = models.CharField(
    max_length=50,
    choices=[
        ('CLEANING', 'Cleaning'),
        ('DELIVERY', 'Delivery'),
        ('LAB', 'Lab Work'),
        ('GENERAL', 'General'),
    ],
    default='GENERAL'
)

    # ⏰ timeline
    due_date = models.DateTimeField(null=True, blank=True)

    # 📊 tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return f"{self.title} → {self.staff.user.email}"