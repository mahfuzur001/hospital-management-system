from rest_framework import serializers
from .models import MedicalRecordModel

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.ReadOnlyField(source='patient.user.get_full_name')
    added_by_name = serializers.ReadOnlyField(source='added_by.user.get_full_name')

    class Meta:
        model = MedicalRecordModel
        fields = [
            'id', 'patient', 'patient_name', 'added_by', 'added_by_name',
            'record_type', 'title', 'description', 'document', 'created_at'
        ]
        read_only_fields = ['added_by', 'created_at']

    def validate_document(self, value):
        # ২ এমবি এর বেশি বড় ফাইল আটকাতে (Industry Standard)
        if value and value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError("File size cannot exceed 2MB.")
        return value