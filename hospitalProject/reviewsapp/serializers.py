from rest_framework import serializers
from .models import ReviewModel


class ReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.user.get_full_name')
    doctor_name = serializers.ReadOnlyField(source='doctor.user.get_full_name')

    class Meta:
        model = ReviewModel
        fields = [
            'id',
            'patient',
            'patient_name',
            'doctor',
            'doctor_name',
            'rating',
            'comment',
            'is_verified',
            'created_at'
        ]
        read_only_fields = ['is_verified', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value