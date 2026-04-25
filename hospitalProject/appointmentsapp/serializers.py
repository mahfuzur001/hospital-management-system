from rest_framework import serializers
from .models import AppointmentModel, PrescriptionModel
from doctorsapp.models import DoctorAvailabilityModel
from django.utils import timezone

# ==========================================
# APPOINTMENT SERIALIZER
# ==========================================
class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.user.get_full_name')
    doctor_name = serializers.ReadOnlyField(source='doctor.user.get_full_name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AppointmentModel
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name', 
            'date', 'time', 'status', 'status_display', 'reason_for_visit', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']

    def validate(self, attrs):
        doctor = attrs.get('doctor')
        patient = attrs.get('patient')
        date = attrs.get('date')
        time = attrs.get('time')

        # ১. অতীত তারিখ কি না চেক করা
        if date < timezone.now().date():
            raise serializers.ValidationError({"date": "আপনি পেছনের কোনো তারিখ বুক করতে পারবেন না।"})

        # ২. সপ্তাহের দিন বের করা (e.g., 'Saturday')
        day_name = date.strftime('%A')

        # ৩. কন্ডিশন ১: ডাক্তার কি ওইদিন এবং ওই সময়ে চেম্বারে আছেন? (Availability Check)
        is_available = DoctorAvailabilityModel.objects.filter(
            doctor=doctor,
            day=day_name,
            start_time__lte=time,
            end_time__gte=time,
            is_active=True
        ).exists()

        if not is_available:
            raise serializers.ValidationError(
                {"time": f"ডাক্তার {day_name} তারিখে এই সময়ে এভেইল্যাবল নন।"}
            )

        # ৪. কন্ডিশন ২: ওই স্লট কি ইতিমধ্যে অন্য কেউ বুক করে ফেলেছে? (Double Booking Check)
        booked_slot = AppointmentModel.objects.filter(
            doctor=doctor,
            date=date,
            time=time,
            status__in=['PENDING', 'CONFIRMED']
        ).exclude(id=self.instance.id if self.instance else None).exists()

        if booked_slot:
            raise serializers.ValidationError("এই স্লটটি ইতিমধ্যে বুক করা হয়েছে।")

        # ৫. কন্ডিশন ৩: পেশেন্ট কি একই সময়ে অন্য ডাক্তারের কাছে অ্যাপয়েন্টমেন্ট নিয়ে রেখেছে?
        patient_busy = AppointmentModel.objects.filter(
            patient=patient,
            date=date,
            time=time,
            status__in=['PENDING', 'CONFIRMED']
        ).exclude(id=self.instance.id if self.instance else None).exists()

        if patient_busy:
            raise serializers.ValidationError("আপনার এই একই সময়ে ইতিমধ্যে অন্য একটি অ্যাপয়েন্টমেন্ট রয়েছে।")

        return attrs


# ==========================================
# PRESCRIPTION SERIALIZER
# ==========================================
class PrescriptionSerializer(serializers.ModelSerializer):
    patient_info = serializers.SerializerMethodField()
    doctor_info = serializers.SerializerMethodField()

    class Meta:
        model = PrescriptionModel
        fields = [
            'id', 'appointment', 'patient_info', 'doctor_info', 
            'symptoms', 'diagnosis', 'medicines', 'advice', 
            'follow_up_date', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_patient_info(self, obj):
        return {
            "name": obj.appointment.patient.user.get_full_name(),
            "age": getattr(obj.appointment.patient, 'age', 'N/A')
        }

    def get_doctor_info(self, obj):
        return {
            "name": obj.appointment.doctor.user.get_full_name(),
            "specialization": getattr(obj.appointment.doctor, 'specialization', 'N/A')
        }

    def validate_appointment(self, value):
        # একটি অ্যাপয়েন্টমেন্টের জন্য শুধুমাত্র একটি প্রেসক্রিপশন হতে পারবে (OneToOne)
        if PrescriptionModel.objects.filter(appointment=value).exists():
            raise serializers.ValidationError("এই অ্যাপয়েন্টমেন্টের জন্য ইতিমধ্যে প্রেসক্রিপশন তৈরি করা হয়েছে।")
        
        # অ্যাপয়েন্টমেন্ট যদি CANCELLED হয় তবে প্রেসক্রিপশন দেওয়া যাবে না
        if value.status == 'CANCELLED':
            raise serializers.ValidationError("বাতিলকৃত অ্যাপয়েন্টমেন্টে প্রেসক্রিপশন দেওয়া সম্ভব নয়।")
            
        return value