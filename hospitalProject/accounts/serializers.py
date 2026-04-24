from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email', 'role', 'mobile_number', 'address']
        read_only_fields = ['role']
        


# Admin Create Admin
class AdminCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    department = serializers.CharField()

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password', 'department']

    def create(self, validated_data):
        department = validated_data.pop('department')

        user = UserModel.objects.create_user(
            role='ADMIN',
            **validated_data
        )

        AdminProfileModel.objects.create(user=user, department=department)

        return user

# Patient Registration Serializer (Public)
class PatientRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role='PATIENT'
        )

        PatientProfileModel.objects.create(user=user)
        return user
    

# Admin Create Doctor
class DoctorCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    speciality = serializers.CharField()
    experience = serializers.IntegerField()
    qualification = serializers.CharField()
    hospital_name = serializers.CharField()
    consultation_fee = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'password',
            'speciality', 'experience', 'qualification',
            'hospital_name', 'consultation_fee'
        ]

    def create(self, validated_data):
        profile_data = {
            'speciality': validated_data.pop('speciality'),
            'experience': validated_data.pop('experience'),
            'qualification': validated_data.pop('qualification'),
            'hospital_name': validated_data.pop('hospital_name'),
            'consultation_fee': validated_data.pop('consultation_fee'),
        }

        user = UserModel.objects.create_user(
            role='DOCTOR',
            **validated_data
        )

        DoctorProfileModel.objects.create(user=user, **profile_data)

        return user
    
    

# Staff Create (Admin only)
class StaffCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    department = serializers.CharField()
    designation = serializers.CharField()

    class Meta:
        model = UserModel
        fields = [
            'username', 'email', 'password',
            'department', 'designation'
        ]

    def create(self, validated_data):
        profile_data = {
            'department': validated_data.pop('department'),
            'designation': validated_data.pop('designation'),
        }

        user = UserModel.objects.create_user(
            role='STAFF',
            **validated_data
        )

        StaffProfileModel.objects.create(user=user, **profile_data)

        return user