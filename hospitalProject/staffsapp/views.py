from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import TaskModel
from .serializers import TaskSerializer



class IsAdminOrDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'DOCTOR']
    
    
    
class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Admin → সব task
        if user.role == 'ADMIN':
            return TaskModel.objects.all()

        # Doctor → তার assign করা task
        elif user.role == 'DOCTOR':
            return TaskModel.objects.filter(assigned_by=user)

        # Staff → নিজের task
        elif user.role == 'STAFF':
            return TaskModel.objects.filter(staff__user=user)

        return TaskModel.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # 🔥 Only admin/doctor can assign task
        if user.role not in ['ADMIN', 'DOCTOR']:
            raise PermissionDenied("Only admin or doctor can assign tasks")

        serializer.save(assigned_by=user)
        
class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return TaskModel.objects.all()

        elif user.role == 'DOCTOR':
            return TaskModel.objects.filter(assigned_by=user)

        elif user.role == 'STAFF':
            return TaskModel.objects.filter(staff__user=user)

        return TaskModel.objects.none()

    def perform_update(self, serializer):
        user = self.request.user

        # 🔥 Staff only update status (not full edit)
        if user.role == 'STAFF':
            allowed_fields = {'status'}

            for field in serializer.validated_data.keys():
                if field not in allowed_fields:
                    raise PermissionDenied("Staff can only update task status")

        serializer.save()