from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import DoctorAvailabilityModel

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    # রিড-অনলি ফিল্ড হিসেবে ডাক্তারের নাম বা ইমেইল দেখানোর জন্য (ঐচ্ছিক)
    doctor_name = serializers.ReadOnlyField(source='doctor.user.get_full_name')

    class Meta:
        model = DoctorAvailabilityModel
        fields = [
            'id', 'doctor', 'doctor_name', 'day', 
            'start_time', 'end_time', 'is_active'
        ]

    def validate(self, attrs):
        """
        সিরিয়ালাইজার লেভেলে মডেলের clean() মেথডকে কল করা।
        এটি মডেলের লেখা ওভারল্যাপ এবং টাইম ভ্যালিডেশন চেক করবে।
        """
        # সাময়িকভাবে একটি ইনস্ট্যান্স তৈরি করে clean() চেক করা
        instance = DoctorAvailabilityModel(**attrs)
        
        try:
            instance.clean()
        except ValidationError as e:
            # মডেলের এরর মেসেজগুলোকে DRF এর ValidationError এ রূপান্তর করা
            raise serializers.ValidationError(e.message_dict if hasattr(e, 'message_dict') else e.messages)
            
        return attrs

    def create(self, validated_data):
        """ডাটা সেভ করার সময় সিরিয়ালাইজার সরাসরি মডেলের লজিক ব্যবহার করবে।"""
        try:
            return super().create(validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)