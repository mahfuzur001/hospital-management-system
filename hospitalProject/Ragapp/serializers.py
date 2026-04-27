from rest_framework import serializers
from .models import DoctorEmbeddingModel


class DoctorEmbeddingSerializer(serializers.ModelSerializer):
    doctor_name = serializers.ReadOnlyField(source='doctor.user.get_full_name')
    doctor_email = serializers.ReadOnlyField(source='doctor.user.email')

    class Meta:
        model = DoctorEmbeddingModel
        fields = [
            'id',
            'doctor',
            'doctor_name',
            'doctor_email',
            'content',
            'embedding_vector',
            'embedding_model',
            'metadata',
            'is_active',
            'created_at',
            'updated_at'
        ]

        # 🔥 user manually edit করতে পারবে না
        read_only_fields = [
            'content',
            'embedding_vector',
            'embedding_model',
            'metadata',
            'created_at',
            'updated_at'
        ]

    # ✅ Fix position
    def validate(self, attrs):
        if not attrs.get('doctor'):
            raise serializers.ValidationError("Doctor is required")
        return attrs