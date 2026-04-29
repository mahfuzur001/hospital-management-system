from rest_framework import serializers
from .models import AppointmentModel, PrescriptionModel
from doctorsapp.models import DoctorAvailabilityModel
from django.utils import timezone


# ==========================================
# APPOINTMENT SERIALIZER (FIXED)
# ==========================================
class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.user.get_full_name')
    doctor_name = serializers.ReadOnlyField(source='doctor.user.get_full_name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = AppointmentModel
        fields = [
            'id', 'patient', 'patient_name', 'doctor', 'doctor_name',
            'date', 'time', 'status', 'status_display',
            'reason_for_visit', 'created_at'
        ]
        read_only_fields = ['status', 'created_at']

    def validate(self, attrs):
        request = self.context.get("request")

        doctor = attrs.get("doctor")
        patient = attrs.get("patient")
        date = attrs.get("date")
        time = attrs.get("time")

        # যদি update হয়
        instance = getattr(self, "instance", None)

        # 1. past date check
        if date < timezone.now().date():
            raise serializers.ValidationError({"date": "Past date booking allowed না।"})

        # 2. FIX: day match issue (important bug fix)
        day_name = date.strftime('%A')

        # 3. availability check (FIXED LOGIC)
        is_available = DoctorAvailabilityModel.objects.filter(
            doctor=doctor,
            day=day_name,
            start_time__lte=time,
            end_time__gte=time,
            is_active=True
        ).exists()

        if not is_available:
            raise serializers.ValidationError({
                "time": f"Doctor {day_name} দিনে এই সময়ে available না।"
            })

        # 4. double booking doctor
        if AppointmentModel.objects.filter(
            doctor=doctor,
            date=date,
            time=time,
            status__in=['PENDING', 'CONFIRMED']
        ).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError("এই slot already booked।")

        # 5. patient conflict
        if AppointmentModel.objects.filter(
            patient=patient,
            date=date,
            time=time,
            status__in=['PENDING', 'CONFIRMED']
        ).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError("আপনার এই সময়ে অন্য appointment আছে।")

        return attrs


# ==========================================
# PRESCRIPTION SERIALIZER (FIXED SAFE)
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
        if PrescriptionModel.objects.filter(appointment=value).exists():
            raise serializers.ValidationError(
                "এই appointment এর জন্য prescription already আছে।"
            )

        if value.status == "CANCELLED":
            raise serializers.ValidationError(
                "Cancelled appointment এ prescription দেওয়া যাবে না।"
            )

        return value
