from django.urls import path
from .views import *

urlpatterns = [
    path('register/', PatientRegisterView.as_view()),
    path('login/', LoginView.as_view()),

    path('admin/create-doctor/', CreateDoctorView.as_view()),
    path('admin/create-staff/', CreateStaffView.as_view()),
    path('admin/create-admin/', CreateAdminView.as_view()),

    path('profile/', ProfileView.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),
]