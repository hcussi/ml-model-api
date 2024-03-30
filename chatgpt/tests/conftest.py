import pytest
from rest_framework.test import APIClient
from rest_framework import HTTP_HEADER_ENCODING
from django.contrib.auth.models import User
import base64
from chatgpt.models import MlJob, MlJobStatus, MlModel
from django.utils import timezone


@pytest.fixture(scope = 'session')
def created_user(django_db_setup, django_db_blocker) -> User:
    """
    Fixture to create test user
    :return:
    """
    with django_db_blocker.unblock():
        return User.objects.create_user(username = 'test', password = 'secret1234')


@pytest.fixture(scope = 'session')
def another_user(django_db_setup, django_db_blocker) -> User:
    """
    Fixture to create another test user
    :return:
    """
    with django_db_blocker.unblock():
        return User.objects.create_user(username = 'test2', password = 'secret1234')


@pytest.fixture(scope = 'session')
def api_client_auth(created_user: User) -> APIClient:
    """
    Fixture to provide an API client with basic auth
    :return: APIClient
    """
    client = APIClient()
    credentials = ('%s:%s' % ('test', 'secret1234'))
    base64_credentials = base64.b64encode(credentials.encode(HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)
    client.credentials(HTTP_AUTHORIZATION = 'Basic %s' % base64_credentials)
    yield client


@pytest.fixture(scope = 'function')
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


@pytest.fixture(scope = 'session')
def mljob_pending(django_db_setup, django_db_blocker, created_user: User) -> MlJob:
    """
    Fixture to create mljob pending
    :return:
    """
    with django_db_blocker.unblock():
        job = MlJob.objects.create(
            user = created_user,
            prompt = 'hello',
            start_time = timezone.now(),
        )
        return job


@pytest.fixture(scope = 'session')
def mljob_done(django_db_setup, django_db_blocker, created_user: User) -> MlJob:
    """
    Fixture to create mljob done
    :return:
    """
    with django_db_blocker.unblock():
        model = MlModel.objects.create(
            user = created_user,
            prompt = 'hello',
            response = 'dummy response from prompt: hello',
            duration = timezone.now() - timezone.now(),
        )

        job = MlJob.objects.create(
            user = created_user,
            mlmodel = model,
            prompt = 'hello',
            status = MlJobStatus.DONE,
            start_time = timezone.now(),
        )
        return job
