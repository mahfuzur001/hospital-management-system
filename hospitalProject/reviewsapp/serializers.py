from rest_framework import serializers
from .models import ReviewModel


class ReviewSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(
        source="patient.user.get_full_name"
    )

    class Meta:
        model = ReviewModel
        fields = [
            "id",
            "doctor",
            "patient",
            "patient_name",
            "rating",
            "comment",
            "is_verified",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "patient",
            "patient_name",
            "is_verified",
            "created_at",
            "updated_at",
        ]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError(
                "Rating must be between 1 and 5"
            )
        return value