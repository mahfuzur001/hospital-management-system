import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from accounts.models import DoctorProfileModel, PatientProfileModel

User = get_user_model()


# =========================
# BASE USER FACTORY
# =========================
class BaseUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@test.com")
    password = factory.LazyFunction(lambda: make_password("password123"))
    is_active = True


# =========================
# PATIENT FACTORY
# =========================
class PatientFactory(BaseUserFactory):
    role = "PATIENT"

    @factory.post_generation
    def create_profile(obj, create, extracted, **kwargs):
        if create:
            PatientProfileModel.objects.get_or_create(user=obj)


# =========================
# DOCTOR FACTORY
# =========================
class DoctorFactory(BaseUserFactory):
    role = "DOCTOR"

    @factory.post_generation
    def create_profile(obj, create, extracted, **kwargs):
        if create:
            DoctorProfileModel.objects.get_or_create(user=obj)


# =========================
# ADMIN FACTORY
# =========================
class AdminFactory(BaseUserFactory):
    role = "ADMIN"
    is_staff = True
    is_superuser = True


# =========================
# USER FACTORY (TEST COMPATIBILITY)
# =========================
class UserFactory(PatientFactory):
    """
    Backward compatibility for old tests
    Acts as Patient by default
    """
    pass
