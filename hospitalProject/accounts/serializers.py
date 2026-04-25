from rest_framework import serializers
from django.db import transaction
from .models import (
    UserModel, 
    AdminProfileModel, 
    DoctorProfileModel, 
    PatientProfileModel, 
    StaffProfileModel
)

# ==========================================
# 1. BASE USER SERIALIZER
# ==========================================
class UserSerializer(serializers.ModelSerializer):
    """লগইন করা ইউজারের সাধারণ তথ্য দেখানোর জন্য সিরিয়ালাইজার।"""
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'role', 'mobile_number', 'address']
        read_only_fields = ['role']


# ==========================================
# 2. PROFILE SERIALIZERS (FOR UPDATES)
# ==========================================
class AdminProfileSerializer(serializers.ModelSerializer):
    """এডমিন প্রোফাইলের তথ্য হ্যান্ডেল করার জন্য।"""
    class Meta:
        model = AdminProfileModel
        exclude = ['user']

class DoctorProfileSerializer(serializers.ModelSerializer):
    """ডাক্তার প্রোফাইলের তথ্য হ্যান্ডেল করার জন্য।"""
    class Meta:
        model = DoctorProfileModel
        exclude = ['user']

class PatientProfileSerializer(serializers.ModelSerializer):
    """পেশেন্ট প্রোফাইলের তথ্য হ্যান্ডেল করার জন্য।"""
    class Meta:
        model = PatientProfileModel
        exclude = ['user']

class StaffProfileSerializer(serializers.ModelSerializer):
    """স্টাফ প্রোফাইলের তথ্য হ্যান্ডেল করার জন্য।"""
    class Meta:
        model = StaffProfileModel
        exclude = ['user']


# ==========================================
# 3. REGISTRATION & ACCOUNT CREATION
# ==========================================

class PatientRegisterSerializer(serializers.ModelSerializer):
    """পেশেন্টদের পাবলিক রেজিস্ট্রেশনের জন্য সিরিয়ালাইজার।"""
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']

    @transaction.atomic
    def create(self, validated_data):
        user = UserModel.objects.create_user(role='PATIENT', **validated_data)
        # Note: যদি সিগন্যাল ব্যবহার করেন তবে প্রোফাইল অটো তৈরি হবে, 
        # অন্যথায় এখানে PatientProfileModel.objects.create(user=user) রাখতে পারেন।
        return user

class AdminCreateSerializer(serializers.ModelSerializer):
    """এডমিন দ্বারা নতুন এডমিন তৈরির জন্য সিরিয়ালাইজার।"""
    password = serializers.CharField(write_only=True)
    department = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'department']

    @transaction.atomic
    def create(self, validated_data):
        department = validated_data.pop('department')
        user = UserModel.objects.create_user(role='ADMIN', **validated_data)
        # প্রোফাইল আপডেট বা তৈরি নিশ্চিত করা
        AdminProfileModel.objects.filter(user=user).update(department=department)
        return user

class DoctorCreateSerializer(serializers.ModelSerializer):
    """এডমিন দ্বারা নতুন ডাক্তার অ্যাকাউন্ট তৈরির জন্য সিরিয়ালাইজার।"""
    password = serializers.CharField(write_only=True)
    speciality = serializers.CharField()
    experience = serializers.IntegerField()
    qualification = serializers.CharField()
    hospital_name = serializers.CharField()
    consultation_fee = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'password', 'speciality', 
            'experience', 'qualification', 'hospital_name', 'consultation_fee'
        ]

    @transaction.atomic
    def create(self, validated_data):
        profile_fields = ['speciality', 'experience', 'qualification', 'hospital_name', 'consultation_fee']
        profile_data = {field: validated_data.pop(field) for field in profile_fields}

        user = UserModel.objects.create_user(role='DOCTOR', **validated_data)
        # সিগন্যালে প্রোফাইল তৈরি হয়ে থাকলে শুধু আপডেট হবে
        DoctorProfileModel.objects.filter(user=user).update(**profile_data)
        return user

class StaffCreateSerializer(serializers.ModelSerializer):
    """এডমিন দ্বারা নতুন স্টাফ অ্যাকাউন্ট তৈরির জন্য সিরিয়ালাইজার।"""
    password = serializers.CharField(write_only=True)
    department = serializers.CharField()
    designation = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'department', 'designation']

    @transaction.atomic
    def create(self, validated_data):
        department = validated_data.pop('department')
        designation = validated_data.pop('designation')
        user = UserModel.objects.create_user(role='STAFF', **validated_data)
        # সিগন্যালে প্রোফাইল তৈরি হয়ে থাকলে শুধু আপডেট হবে
        StaffProfileModel.objects.filter(user=user).update(department=department, designation=designation)
        return user