import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_patient_register(api_client):
    url = reverse('patient-register')

    data = {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "password123"
    }

    response = api_client.post(url, data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_login(api_client):
    # register first
    api_client.post(reverse('patient-register'), {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "password123"
    })

    url = reverse('token_obtain_pair')

    response = api_client.post(url, {
        "username": "testuser",
        "password": "password123"
    })

    assert response.status_code == 200
    assert "access" in response.data


@pytest.mark.django_db
def test_invalid_login(api_client):
    url = reverse('token_obtain_pair')

    response = api_client.post(url, {
        "username": "wrong",
        "password": "wrong"
    })

    # JWT সাধারণত 401 দেয়
    assert response.status_code == 401
