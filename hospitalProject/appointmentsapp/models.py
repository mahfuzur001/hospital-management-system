from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import DoctorProfileModel, PatientProfileModel

class AppointmentModel(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'), # অ্যাপয়েন্টমেন্ট শেষ হলে এটি প্রয়োজন
        ('CANCELLED', 'Cancelled'),
    )

    patient = models.ForeignKey(
        PatientProfileModel, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        DoctorProfileModel, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    
    # ইন্ডাস্ট্রি স্ট্যান্ডার্ড ফিল্ডস
    reason_for_visit = models.TextField(blank=True, help_text="পেশেন্টের সমস্যার সংক্ষিপ্ত বিবরণ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        # একই সময়ে একই ডাক্তারের একাধিক অ্যাপয়েন্টমেন্ট রোধ করতে
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"Appt: {self.patient.user.get_full_name()} with {self.doctor.user.get_full_name()} on {self.date}"

    def clean(self):
        # ১. অতীত তারিখের অ্যাপয়েন্টমেন্ট রোধ
        from django.utils import timezone
        if self.date < timezone.now().date():
            raise ValidationError("You cannot book an appointment for a past date.")

        # ২. ডাক্তার ওই দিন এবং সময়ে এভেইল্যাবল কি না তা চেক করার লজিক (DoctorAvailabilityModel থেকে)
        # এটি আমরা সিরিয়ালাইজার বা ভিউতে আরও বিস্তারিত হ্যান্ডেল করতে পারি।


class PrescriptionModel(models.Model):
    # OneToOneField ঠিক আছে, তবে related_name যোগ করা ভালো
    appointment = models.OneToOneField(
        AppointmentModel, 
        on_delete=models.CASCADE, 
        related_name='prescription'
    )
    
    # ডাটাবেস ডিজাইন অনুযায়ী ঔষধগুলোকে আলাদা ফিল্ডে রাখা ভালো
    symptoms = models.TextField(help_text="পেশেন্টের লক্ষণসমূহ")
    diagnosis = models.TextField(help_text="রোগ নির্ণয়")
    medicines = models.TextField(help_text="ঔষধের তালিকা (JSON বা ফরম্যাটেড টেক্সট)")
    advice = models.TextField(blank=True, help_text="ডাক্তারের বিশেষ উপদেশ")
    
    follow_up_date = models.DateField(null=True, blank=True, help_text="পরবর্তী সাক্ষাতের তারিখ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"

    def __str__(self):
        return f"Prescription for {self.appointment.patient.user.get_full_name()}"