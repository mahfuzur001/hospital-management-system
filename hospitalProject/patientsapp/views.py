from rest_framework import generics, permissions
from .models import MedicalRecordModel
from .serializers import MedicalRecordSerializer


# =========================
# PERMISSION CLASS
# =========================
class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "DOCTOR"


# =========================
# VIEW
# =========================
class MedicalRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return MedicalRecordModel.objects.all()

        if user.role == 'DOCTOR':
            # চাইলে future এ filter করা যাবে patient-based
            return MedicalRecordModel.objects.all()

        if user.role == 'PATIENT':
            return MedicalRecordModel.objects.filter(patient__user=user)

        return MedicalRecordModel.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'DOCTOR':
            serializer.save(added_by=user.doctor_profile)
        else:
            serializer.save()
