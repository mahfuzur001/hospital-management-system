from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from appointmentsapp.models import AppointmentModel
from .models import ReviewModel
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        doctor_id = self.request.query_params.get('doctor')

        if doctor_id:
            return ReviewModel.objects.filter(doctor_id=doctor_id)

        return ReviewModel.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        doctor = serializer.validated_data.get('doctor')

        # 🔒 Only patient can review
        if user.role != "PATIENT":
            raise PermissionDenied("Only patients can create reviews")

        # 🔥 Check appointment exists
        has_appointment = AppointmentModel.objects.filter(
            patient=user.patient_profile,
            doctor=doctor,
            status='COMPLETED'
        ).exists()

        if not has_appointment:
            raise PermissionDenied("You can only review doctors you have visited")

        # ✅ Save review
        serializer.save(
            patient=user.patient_profile,
            is_verified=True
        )