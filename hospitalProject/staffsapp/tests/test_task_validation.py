import pytest
from django.urls import reverse
from django.utils import timezone
from staffsapp.tests.factories import (
    AdminFactory,
    StaffProfileFactory
)


@pytest.mark.django_db
def test_due_date_cannot_be_past(api_client):
    admin = AdminFactory()
    staff_profile = StaffProfileFactory()

    api_client.force_authenticate(user=admin)

    url = reverse("task-list-create")

    data = {
        "staff": staff_profile.id,
        "title": "Past Task",
        "category": "GENERAL",
        "due_date": timezone.now() - timezone.timedelta(days=1)
    }

    response = api_client.post(url, data)

    assert response.status_code == 400
    assert "due_date" in response.data