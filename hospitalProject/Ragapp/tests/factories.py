import factory
from accounts.models import DoctorProfileModel, UserModel
from Ragapp.models import DoctorEmbeddingModel


# =========================
# 👤 USER FACTORY
# =========================
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Sequence(lambda n: f"user_{n}@test.com")
    role = "DOCTOR"


# =========================
# 👨‍⚕️ DOCTOR PROFILE FACTORY
# =========================
class DoctorProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DoctorProfileModel
        django_get_or_create = ("user",)

    user = factory.SubFactory(UserFactory)

    speciality = "Cardiology"
    experience = 5
    qualification = "MBBS"
    hospital_name = "Test Hospital"
    consultation_fee = 500.00


# =========================
# 🧠 EMBEDDING FACTORY (FIXED)
# =========================
class DoctorEmbeddingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DoctorEmbeddingModel

    doctor = factory.SubFactory(DoctorProfileFactory)
    content = factory.Sequence(lambda n: f"Heart specialist doctor {n}")
    embedding_model = "test-model"
    embedding_vector = [0.1, 0.2, 0.3]
    metadata = {"rating": 4.5}
    is_active = True