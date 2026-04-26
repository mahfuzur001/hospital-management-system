from rest_framework import serializers
from django.utils import timezone
from .models import TaskModel


class TaskSerializer(serializers.ModelSerializer):
    staff_name = serializers.ReadOnlyField(source='staff.user.get_full_name')
    assigned_by_name = serializers.ReadOnlyField(source='assigned_by.get_full_name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = TaskModel
        fields = [
            'id',
            'staff',
            'staff_name',
            'assigned_by',
            'assigned_by_name',
            'title',
            'description',
            'category',
            'category_display',
            'status',
            'status_display',
            'priority',
            'priority_display',
            'due_date',
            'created_at',
            'updated_at',
            'completed_at'
        ]
        read_only_fields = [
            'assigned_by',
            'created_at',
            'updated_at',
            'completed_at'
        ]

    # 🔥 Validation
    def validate(self, attrs):
        due_date = attrs.get('due_date')

        if due_date and due_date < timezone.now():
            raise serializers.ValidationError({
                "due_date": "Due date cannot be in the past"
            })

        return attrs

    # 🔥 Auto handle completed_at
    def update(self, instance, validated_data):
        status = validated_data.get('status')

        # যদি DONE হয় → completed_at set হবে
        if status == 'DONE' and instance.status != 'DONE':
            instance.completed_at = timezone.now()

        # যদি DONE থেকে অন্য status এ যায় → reset
        elif status != 'DONE':
            instance.completed_at = None

        return super().update(instance, validated_data)