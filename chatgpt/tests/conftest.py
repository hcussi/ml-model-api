import pytest
from rest_framework.test import APIClient
from rest_framework import HTTP_HEADER_ENCODING
from django.contrib.auth.models import User
import base64
from chatgpt.models import MlJob, MlJobStatus


@pytest.fixture(scope = 'session')
def created_user(django_db_setup, django_db_blocker) -> None:
    """
    Fixture to create test user
    :return:
    """
    with django_db_blocker.unblock():
        User.objects.create_user(username = 'test', password = 'secret1234')


@pytest.fixture(scope = 'session')
def api_client_auth(created_user) -> APIClient:
    """
    Fixture to provide an API client with basic auth
    :return: APIClient
    """
    client = APIClient()
    credentials = ('%s:%s' % ('test', 'secret1234'))
    base64_credentials = base64.b64encode(credentials.encode(HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)
    client.credentials(HTTP_AUTHORIZATION = 'Basic %s' % base64_credentials)
    yield client


@pytest.fixture(scope = 'session')
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    yield APIClient()


@pytest.fixture(scope = 'function')
def mock_mljob(mocker):
    mock = MlJob(id=123, prompt='hello', status=MlJobStatus.PENDING)
    mocker.patch('chatgpt.models.MlJob.objects.create', return_value=mock)
