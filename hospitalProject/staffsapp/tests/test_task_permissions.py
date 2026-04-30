import pytest
from django.urls import reverse
from staffsapp.tests.factories import (
    StaffFactory,
    StaffProfileFactory,
    TaskFactory
)


@pytest.mark.django_db
def test_staff_cannot_create_task(api_client):
    staff_user = StaffFactory()
    staff_profile = StaffProfileFactory()

    api_client.force_authenticate(user=staff_user)

    url = reverse("task-list-create")

    data = {
        "staff": staff_profile.id,
        "title": "Unauthorized Task",
        "category": "GENERAL"
    }

    response = api_client.post(url, data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_staff_can_only_update_status(api_client):
    staff_user = StaffFactory()
    staff_profile = StaffProfileFactory(user=staff_user)

    task = TaskFactory(staff=staff_profile)

    api_client.force_authenticate(user=staff_user)

    url = reverse("task-detail", args=[task.id])

    response = api_client.patch(url, {
        "status": "DONE"
    })

    assert response.status_code == 200


@pytest.mark.django_db
def test_staff_cannot_edit_title(api_client):
    staff_user = StaffFactory()
    staff_profile = StaffProfileFactory(user=staff_user)

    task = TaskFactory(staff=staff_profile)

    api_client.force_authenticate(user=staff_user)

    url = reverse("task-detail", args=[task.id])

    response = api_client.patch(url, {
        "title": "Hacked Title"
    })

    assert response.status_code == 403