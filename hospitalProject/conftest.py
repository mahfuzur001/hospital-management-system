import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()



import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(db):
    from accounts.tests.factories import PatientFactory

    user = PatientFactory()
    client = APIClient()
    client.force_authenticate(user=user)
    return client
