from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import DoctorProfileModel

class DoctorAvailabilityModel(models.Model):
    # সপ্তাহের দিনগুলোর জন্য চয়েস
    WEEK_DAYS = (
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    )

    doctor = models.ForeignKey(
        DoctorProfileModel, 
        on_delete=models.CASCADE, 
        related_name='availabilities'
    )
    day = models.CharField(max_length=20, choices=WEEK_DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    # অতিরিক্ত কাজের জন্য কিছু প্রয়োজনীয় ফিল্ড
    is_active = models.BooleanField(default=True, help_text="ডাক্তার কি এই সময়ে চেম্বারে বসবেন?",null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = "Doctor Availability"
        verbose_name_plural = "Doctor Availabilities"
        # একই দিনে একই সময়ে ডুপ্লিকেট এন্ট্রি রোধ করতে
        unique_together = ('doctor', 'day', 'start_time', 'end_time')
        ordering = ['day', 'start_time']

    def __str__(self):
        return f"{self.doctor.user.get_full_name()} - {self.day} ({self.start_time} - {self.end_time})"

    def clean(self):
        """
        লজিক্যাল ভ্যালিডেশন: 
        ১. শেষ সময় অবশ্যই শুরু সময়ের পরে হতে হবে।
        ২. একই দিনে সময়ের ওভারল্যাপ চেক।
        """
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")

        # ওভারল্যাপ চেক করার লজিক
        overlapping_availabilities = DoctorAvailabilityModel.objects.filter(
            doctor=self.doctor,
            day=self.day,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(pk=self.pk)

        if overlapping_availabilities.exists():
            raise ValidationError(f"This time slot overlaps with an existing availability on {self.day}.")

    def save(self, *args, **kwargs):
        self.full_clean() # সেভ করার আগে clean() মেথড কল করা বাধ্যতামূলক
        super().save(*args, **kwargs)