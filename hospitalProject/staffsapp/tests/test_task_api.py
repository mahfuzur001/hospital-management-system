import pytest
from django.urls import reverse
from staffsapp.tests.factories import (
    StaffFactory,
    AdminFactory,
    DoctorFactory,
    StaffProfileFactory,
    TaskFactory
)


@pytest.mark.django_db
def test_admin_can_create_task(api_client):
    admin = AdminFactory()
    staff_profile = StaffProfileFactory()

    api_client.force_authenticate(user=admin)

    url = reverse("task-list-create")

    data = {
        "staff": staff_profile.id,
        "title": "Clean ICU",
        "description": "Clean room 302",
        "category": "CLEANING",
        "priority": "HIGH"
    }

    response = api_client.post(url, data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_staff_can_view_own_tasks(api_client):
    staff_user = StaffFactory()
    staff_profile = StaffProfileFactory(user=staff_user)

    TaskFactory(staff=staff_profile)

    api_client.force_authenticate(user=staff_user)

    url = reverse("task-list-create")
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 1