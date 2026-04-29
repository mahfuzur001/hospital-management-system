import factory
from accounts.models import UserModel, PatientProfileModel, DoctorProfileModel


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@test.com")
    role = "PATIENT"

    @factory.post_generation
    def create_profile(self, create, extracted, **kwargs):
        if not create:
            return

        if self.role == "PATIENT":
            PatientProfileModel.objects.create(user=self)
        elif self.role == "DOCTOR":
            DoctorProfileModel.objects.create(user=self)
