from django.db import models
from accounts.models import StaffProfileModel


class TaskModel(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('DONE', 'Done'),
    )

    staff = models.ForeignKey(StaffProfileModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')