import factory
from django.utils import timezone
from datetime import timedelta

from accounts.tests.factories import UserFactory
from accounts.models import StaffProfileModel
from staffsapp.models import TaskModel


# ======================================================
# 👨‍⚕️ STAFF USER FACTORY
# ======================================================
class StaffFactory(UserFactory):
    role = "STAFF"

    username = factory.Sequence(lambda n: f"staff{n}")
    email = factory.Sequence(lambda n: f"staff{n}@test.com")


# ======================================================
# 👤 STAFF PROFILE FACTORY (FIXED)
# ======================================================
class StaffProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StaffProfileModel
        django_get_or_create = ("user",)   # ✅ IMPORTANT FIX

    user = factory.SubFactory(StaffFactory)
    department = factory.Faker("random_element", elements=["Cardiology", "Neurology", "Orthopedic"])
    designation = factory.Faker("random_element", elements=["Doctor", "Nurse", "Technician"])


# ======================================================
# 👨‍💼 ADMIN FACTORY
# ======================================================
class AdminFactory(UserFactory):
    role = "ADMIN"

    username = factory.Sequence(lambda n: f"admin{n}")
    email = factory.Sequence(lambda n: f"admin{n}@test.com")


# ======================================================
# 👨‍⚕️ DOCTOR FACTORY
# ======================================================
class DoctorFactory(UserFactory):
    role = "DOCTOR"

    username = factory.Sequence(lambda n: f"doctor{n}")
    email = factory.Sequence(lambda n: f"doctor{n}@test.com")


# ======================================================
# 📌 TASK FACTORY
# ======================================================
class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TaskModel

    staff = factory.SubFactory(StaffProfileFactory)
    assigned_by = factory.SubFactory(AdminFactory)

    title = factory.Sequence(lambda n: f"Task {n}")
    description = "Test task description"

    category = factory.Faker("random_element", elements=["GENERAL", "URGENT", "DAILY"])
    priority = factory.Faker("random_element", elements=["LOW", "MEDIUM", "HIGH"])
    status = "PENDING"

    due_date = factory.LazyFunction(
        lambda: timezone.now() + timedelta(days=2)
    )