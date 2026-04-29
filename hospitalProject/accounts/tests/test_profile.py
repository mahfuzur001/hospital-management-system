import pytest
from django.urls import reverse
from accounts.tests.factories import UserFactory


@pytest.mark.django_db
def test_get_profile(api_client):
    user = UserFactory()

    api_client.force_authenticate(user=user)

    url = reverse('user-profile')
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["username"] == user.username


@pytest.mark.django_db
def test_update_profile(api_client):
    user = UserFactory()

    api_client.force_authenticate(user=user)

    url = reverse('user-profile')

    response = api_client.patch(url, {
        "mobile_number": "01700000000",
        "profile_details": {}
    }, format='json')

    assert response.status_code == 200


@pytest.mark.django_db
def test_patient_profile_created():
    user = UserFactory(role="PATIENT")

    assert hasattr(user, "patient_profile")


@pytest.mark.django_db
def test_profile_without_login(api_client):
    url = reverse('user-profile')

    response = api_client.get(url)

    assert response.status_code == 401
