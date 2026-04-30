from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from appointmentsapp.models import AppointmentModel
from .models import ReviewModel
from .serializers import ReviewSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        doctor_id = self.request.query_params.get("doctor")

        queryset = ReviewModel.objects.select_related(
            "doctor__user",
            "patient__user"
        )

        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        return queryset

    # 🔥 IMPORTANT:
    # permission check before serializer validation
    def create(self, request, *args, **kwargs):
        user = request.user

        if user.role != "PATIENT":
            raise PermissionDenied("Only patients can create reviews")

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = self.request.user
        doctor = serializer.validated_data.get("doctor")

        # 🔥 completed appointment required
        has_appointment = AppointmentModel.objects.filter(
            patient=user.patient_profile,
            doctor=doctor,
            status="COMPLETED"
        ).exists()

        if not has_appointment:
            raise PermissionDenied(
                "You can only review doctors you have visited"
            )

        serializer.save(
            patient=user.patient_profile,
            is_verified=True
        )