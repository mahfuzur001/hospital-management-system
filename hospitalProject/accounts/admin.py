from django.contrib import admin
from .models import UserModel, AdminProfileModel, DoctorProfileModel, PatientProfileModel, StaffProfileModel
# Register your models here.
admin.site.register([UserModel, AdminProfileModel, DoctorProfileModel, PatientProfileModel, StaffProfileModel])