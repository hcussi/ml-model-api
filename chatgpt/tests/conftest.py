import pytest
from rest_framework.test import APIClient
from rest_framework import HTTP_HEADER_ENCODING
from django.contrib.auth.models import User
import base64


@pytest.fixture(scope = 'function')
def api_client() -> APIClient:
    """
    Fixture to provide an API client
    :return: APIClient
    """
    yield APIClient()


@pytest.fixture(scope = 'session')
def created_user(django_db_setup, django_db_blocker) -> None:
    """
    Fixture to create test user
    :return:
    """
    with django_db_blocker.unblock():
        User.objects.create_user(username = 'test', password = 'secret1234')


@pytest.fixture(scope = 'session')
def auth_header():
    """
    Fixture to create the basic auth header for the test user
    :return: the basic auth header value
    """
    credentials = ('%s:%s' % ('test', 'secret1234'))
    base64_credentials = base64.b64encode(credentials.encode(HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)
    return 'Basic %s' % base64_credentials
