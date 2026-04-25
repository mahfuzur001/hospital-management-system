from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import DoctorAvailabilityModel
from .serializers import DoctorAvailabilitySerializer

# ==========================================
# CUSTOM PERMISSION (Doctor Owner or Admin)
# ==========================================
class IsDoctorOwnerOrAdmin(permissions.BasePermission):
    """
    শুধুমাত্র স্লটের মালিক (ডাক্তার) অথবা এডমিন স্লট এডিট/ডিলিট করতে পারবে।
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.role == 'ADMIN':
            return True
        return obj.doctor.user == request.user

# ==========================================
# DOCTOR AVAILABILITY VIEWS
# ==========================================

class DoctorAvailabilityListCreateView(generics.ListCreateAPIView):
    """
    GET: সব স্লট দেখা।
    POST: ডাক্তার (নিজের জন্য) অথবা এডমিন (যেকোনো ডাক্তারের জন্য) স্লট তৈরি করবেন।
    """
    queryset = DoctorAvailabilityModel.objects.filter(is_active=True)
    serializer_class = DoctorAvailabilitySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        user = self.request.user
        
        if user.role == 'ADMIN':
            if 'doctor' not in self.request.data:
                raise ValidationError({"doctor": "Admin must provide a doctor ID to create a slot."})
            serializer.save() 
            
        elif user.role == 'DOCTOR':
            if hasattr(user, 'doctor_profile'):
                serializer.save(doctor=user.doctor_profile)
            else:
                raise ValidationError("Doctor profile not found.")
        else:
            raise ValidationError("Only doctors and admins can create availability slots.")

class DoctorAvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PUT, PATCH, DELETE: মালিক ডাক্তার অথবা এডমিন এক্সেস পাবে।
    """
    queryset = DoctorAvailabilityModel.objects.all()
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOwnerOrAdmin]

# ============================================================
# MISSING VIEW: নির্দিষ্ট ডাক্তারের স্লট দেখা (এই অংশটি যোগ করা হয়েছে)
# ============================================================
class SpecificDoctorAvailabilityView(generics.ListAPIView):
    """
    পেশেন্টরা যখন কোনো নির্দিষ্ট ডাক্তারের প্রোফাইলে যাবে, তখন তার স্লটগুলো দেখাবে।
    URL Example: /api/doctors/1/availability/
    """
    serializer_class = DoctorAvailabilitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return DoctorAvailabilityModel.objects.filter(doctor_id=doctor_id, is_active=True)