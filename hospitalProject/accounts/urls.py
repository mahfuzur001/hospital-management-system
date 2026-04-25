from django.urls import path
from .views import (
    PatientRegisterView,
    LoginView,
    CreateDoctorView,
    CreateStaffView,
    CreateAdminView,
    UserProfileView,
)

urlpatterns = [
    # --- Public Endpoints ---
    path('register/', PatientRegisterView.as_view(), name='patient-register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),

    # --- Admin Only Endpoints (Management) ---
    path('admin/create-doctor/', CreateDoctorView.as_view(), name='admin-create-doctor'),
    path('admin/create-staff/', CreateStaffView.as_view(), name='admin-create-staff'),
    path('admin/create-admin/', CreateAdminView.as_view(), name='admin-create-admin'),

    # --- Authenticated User Endpoints ---
    # এই একটি ইউআরএল দিয়েই GET (view) এবং PATCH/PUT (update) করা যাবে
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]