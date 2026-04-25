from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import AppointmentModel, PrescriptionModel
from .serializers import AppointmentSerializer, PrescriptionSerializer

# ==========================================
# CUSTOM PERMISSIONS
# ==========================================
class IsDoctorOwner(permissions.BasePermission):
    """শুধুমাত্র অ্যাপয়েন্টমেন্টের ডাক্তার প্রেসক্রিপশন তৈরি/এডিট করতে পারবেন।"""
    def has_object_permission(self, request, view, obj):
        return obj.doctor.user == request.user

# ==========================================
# APPOINTMENT VIEWS
# ==========================================

class AppointmentListCreateView(generics.ListCreateAPIView):
    """
    GET: ইউজার রোল অনুযায়ী অ্যাপয়েন্টমেন্ট লিস্ট দেখাবে।
    POST: নতুন অ্যাপয়েন্টমেন্ট বুক করবে।
    """
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return AppointmentModel.objects.all()
        elif user.role == 'DOCTOR':
            return AppointmentModel.objects.filter(doctor__user=user)
        # পেশেন্ট শুধুমাত্র নিজের বুক করা অ্যাপয়েন্টমেন্ট দেখবে
        return AppointmentModel.objects.filter(patient__user=user)

    def perform_create(self, serializer):
        # যদি ইউজার PATIENT হয়, তবে তার প্রোফাইল অটোমেটিক সেট হবে
        if self.request.user.role == 'PATIENT':
            serializer.save(patient=self.request.user.patient_profile)
        else:
            serializer.save()

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """অ্যাপয়েন্টমেন্ট ডিটেইলস দেখা, আপডেট করা বা বাতিল করা।"""
    queryset = AppointmentModel.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return AppointmentModel.objects.all()
        elif user.role == 'DOCTOR':
            return AppointmentModel.objects.filter(doctor__user=user)
        return AppointmentModel.objects.filter(patient__user=user)


# ==========================================
# PRESCRIPTION VIEWS
# ==========================================

class PrescriptionCreateView(generics.CreateAPIView):
    """শুধুমাত্র ডাক্তার অ্যাপয়েন্টমেন্ট শেষ করে প্রেসক্রিপশন তৈরি করবেন।"""
    queryset = PrescriptionModel.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        appointment = serializer.validated_data['appointment']
        
        # ১. নিরাপত্তা চেক: এই অ্যাপয়েন্টমেন্টের ডাক্তার কি বর্তমান ইউজার?
        if appointment.doctor.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("আপনি অন্য ডাক্তারের অ্যাপয়েন্টমেন্টে প্রেসক্রিপশন দিতে পারবেন না।")
        
        # ২. প্রেসক্রিপশন তৈরি হলে অ্যাপয়েন্টমেন্ট স্ট্যাটাস 'COMPLETED' করে দেওয়া
        serializer.save()
        appointment.status = 'COMPLETED'
        appointment.save()

class PrescriptionDetailView(generics.RetrieveUpdateAPIView):
    """প্রেসক্রিপশন দেখা এবং আপডেট করা।"""
    queryset = PrescriptionModel.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return PrescriptionModel.objects.all()
        elif user.role == 'DOCTOR':
            return PrescriptionModel.objects.filter(appointment__doctor__user=user)
        # পেশেন্ট শুধুমাত্র নিজের প্রেসক্রিপশন দেখবে
        return PrescriptionModel.objects.filter(appointment__patient__user=user)