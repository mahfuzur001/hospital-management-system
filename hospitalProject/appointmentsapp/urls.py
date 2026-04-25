from django.urls import path
from .views import (
    AppointmentListCreateView, AppointmentDetailView,
    PrescriptionCreateView, PrescriptionDetailView
)

urlpatterns = [
    path('appointments/', AppointmentListCreateView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('prescriptions/', PrescriptionCreateView.as_view(), name='prescription-create'),
    path('prescriptions/<int:pk>/', PrescriptionDetailView.as_view(), name='prescription-detail'),
]