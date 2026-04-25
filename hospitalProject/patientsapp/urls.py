from django.urls import path
from .views import MedicalRecordListCreateView

urlpatterns = [
    # মেডিকেল রেকর্ড দেখা এবং তৈরি করার এন্ডপয়েন্ট
    path('medical-records/', MedicalRecordListCreateView.as_view(), name='medical-record-list'),
]