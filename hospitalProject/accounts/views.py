from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.views import TokenObtainPairView # type: ignore

from .serializers import (
    UserSerializer, 
    PatientRegisterSerializer, 
    DoctorCreateSerializer, 
    StaffCreateSerializer, 
    AdminCreateSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer,
    StaffProfileSerializer,
    AdminProfileSerializer
)
from .models import UserModel

# ---------------------------------------------------------
# CUSTOM PERMISSION CLASSES
# ---------------------------------------------------------

# উদাহরণস্বরূপ, শুধুমাত্র এডমিনরা এই এন্ডপয়েন্টে অ্যাক্সেস পাবে এমন একটি পারমিশন ক্লাস:
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff) # অথবা আপনার কাস্টম লজিক

class IsDoctor(permissions.BasePermission):
    """শুধুমাত্র ডাক্তার এক্সেস পাবে।"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "DOCTOR"

# ---------------------------------------------------------
# AUTHENTICATION & REGISTRATION VIEWS
# ---------------------------------------------------------

class LoginView(TokenObtainPairView):
    """JWT টোকেন প্রদান করে লগইন সম্পন্ন করে।"""
    pass

class PatientRegisterView(APIView):
    """পেশেন্টরা পাবলিকলি এই এন্ডপয়েন্ট ব্যবহার করে একাউন্ট খুলতে পারবে।"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PatientRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Patient registered successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------
# ADMIN MANAGEMENT VIEWS (ADMIN ONLY)
# ---------------------------------------------------------

class CreateDoctorView(APIView):
    """এডমিন নতুন ডাক্তার অ্যাকাউন্ট তৈরি করতে পারবে।"""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = DoctorCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Doctor created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateStaffView(APIView):
    """এডমিন নতুন স্টাফ অ্যাকাউন্ট তৈরি করতে পারবে।"""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = StaffCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Staff created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateAdminView(APIView):
    """এডমিন নতুন এডমিন অ্যাকাউন্ট তৈরি করতে পারবে।"""
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = AdminCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------
# USER PROFILE & UPDATE VIEWS (LOGGED-IN USER)
# ---------------------------------------------------------

class UserProfileView(APIView):
    """লগইন করা ইউজারের প্রোফাইল দেখা এবং রোল অনুযায়ী আংশিক আপডেট করা।"""
    permission_classes = [permissions.IsAuthenticated]

    def get_profile_serializer(self, user, data=None, partial=False):
        """রোলের ওপর ভিত্তি করে সঠিক প্রোফাইল সিরিয়ালাইজার রিটার্ন করে।"""
        
        # ১. আগে ইউজারের রোল অনুযায়ী প্রোফাইল অবজেক্ট ও সঠিক সিরিয়ালাইজার ক্লাস খুঁজে বের করা
        profile_obj = None
        serializer_class = None

        if user.role == 'ADMIN':
            profile_obj = getattr(user, 'admin_profile', None)
            serializer_class = AdminProfileSerializer
        elif user.role == 'DOCTOR':
            profile_obj = getattr(user, 'doctor_profile', None)
            serializer_class = DoctorProfileSerializer
        elif user.role == 'PATIENT':
            profile_obj = getattr(user, 'patient_profile', None)
            serializer_class = PatientProfileSerializer
        elif user.role == 'STAFF':
            profile_obj = getattr(user, 'staff_profile', None)
            serializer_class = StaffProfileSerializer

        if not serializer_class or not profile_obj:
            return None

        # ২. প্রধান সমাধান: GET রিকোয়েস্টের জন্য (যখন data=None)
        if data is None:
            return serializer_class(instance=profile_obj)
        
        # ৩. PATCH রিকোয়েস্টের জন্য (যখন data প্রদান করা হয়)
        return serializer_class(instance=profile_obj, data=data, partial=partial)

    def get(self, request):
        """ইউজারের বেসিক ডাটা ও প্রোফাইলের বিস্তারিত ডাটা প্রদান করে।"""
        user_serializer = UserSerializer(request.user)
        response_data = user_serializer.data
        
        # এখানে এখন আর এরর আসবে না কারণ data=None হলে আমরা শুধু instance পাঠাচ্ছি
        profile_serializer = self.get_profile_serializer(request.user)
        
        if profile_serializer:
            response_data['profile_details'] = profile_serializer.data
        else:
            response_data['profile_details'] = None
            
        return Response(response_data)

    def patch(self, request):
        """ইউজার মডেল ও প্রোফাইল মডেল একসাথে আপডেট করে।"""
        user = request.user
        user_serializer = UserSerializer(user, data=request.data, partial=True)
        
        if user_serializer.is_valid():
            user_serializer.save()
            
            profile_data = request.data.get('profile_details')
            if profile_data:
                profile_serializer = self.get_profile_serializer(user, data=profile_data, partial=True)
                
                if profile_serializer:
                    # এখানে .is_valid() কল করা হচ্ছে, তাই কোনো সমস্যা হবে না
                    if profile_serializer.is_valid():
                        profile_serializer.save()
                    else:
                        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # আপডেট শেষে নতুন ডাটা রিটার্ন করা
            return self.get(request)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)