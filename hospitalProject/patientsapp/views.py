from rest_framework import generics, permissions
from .models import MedicalRecordModel
from .serializers import MedicalRecordSerializer

class MedicalRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = MedicalRecordSerializer

    def get_queryset(self):
        user = self.request.user
        # এডমিন সব দেখবে
        if user.role == 'ADMIN':
            return MedicalRecordModel.objects.all()
        # ডাক্তার তার পেশেন্টদের রেকর্ড দেখবে
        elif user.role == 'DOCTOR':
            return MedicalRecordModel.objects.all() # অথবা নির্দিষ্ট লজিক
        # পেশেন্ট শুধু নিজের রেকর্ড দেখবে
        return MedicalRecordModel.objects.filter(patient__user=user)

    def perform_create(self, serializer):
        # রেকর্ড কে যোগ করছে তা অটোমেটিক সেট করা
        if self.request.user.role == 'DOCTOR':
            serializer.save(added_by=self.request.user.doctor_profile)
        else:
            serializer.save()