from django.urls import path
from .views import (
    DoctorAvailabilityListCreateView, 
    DoctorAvailabilityDetailView,
    SpecificDoctorAvailabilityView
)

urlpatterns = [
    # সব স্লট দেখা বা নতুন তৈরি (ডাক্তারের জন্য)
    path('availability/', DoctorAvailabilityListCreateView.as_view(), name='availability-list'),
    # নির্দিষ্ট স্লট এডিট বা ডিলিট
    path('availability/<int:pk>/', DoctorAvailabilityDetailView.as_view(), name='availability-detail'),
    # কোনো নির্দিষ্ট ডাক্তারের সব স্লট দেখা (পেশেন্টের জন্য)
    path('<int:doctor_id>/availability/', SpecificDoctorAvailabilityView.as_view(), name='doctor-specific-availability'),
]