from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.response import Response
import pytest


@pytest.mark.django_db
def test_call_model(api_client: APIClient, auth_header: str, created_user: None) -> None:
    """
    Test success call_model API endpoint
    :param api_client: APiClient
    :return: None
    """
    response: Response = api_client.post(
        '/api/v1/call_model/',
        data = { 'prompt': 'hello' },
        format = 'json',
        HTTP_AUTHORIZATION=auth_header,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content_type == 'application/json'
    assert response.data['response'] == 'dummy response from prompt: hello'


def test_call_model_without_auth(api_client: APIClient) -> None:
    """
    Test success call_model API endpoint
    :param api_client: APiClient
    :return: None
    """
    response: Response = api_client.post(
        '/api/v1/call_model/',
        data = { 'prompt': 'hello' },
        format = 'json',
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_call_model_without_params(api_client: APIClient, auth_header: str, created_user: None) -> None:
    """
    Test the update task API
    :param api_client: APiClient
    :return: None
    """
    response: Response = api_client.post(
        '/api/v1/call_model/',
        format = 'json',
        HTTP_AUTHORIZATION = auth_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_call_model_without_wrong_params(api_client: APIClient, auth_header: str, created_user: None) -> None:
    """
    Test the update task API
    :param api_client: APiClient
    :return: None
    """
    response: Response = api_client.post(
        '/api/v1/call_model/',
        data = { 'foo': 'hello' },
        format = 'json',
        HTTP_AUTHORIZATION = auth_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_health(api_client: APIClient) -> None:
    """
    Test success health API endpoint
    :param api_client: APiClient
    :return: None
    """
    response: Response = api_client.get('/api/v1/health/')
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_unexisting_endpoint(api_client: APIClient) -> None:
    """
    Test unexisting API endpoint
    :param api_client: APiClient
    :return: None
    """
    response: Response = api_client.get('/api/v1/foo/')
    assert response.status_code == status.HTTP_404_NOT_FOUND
