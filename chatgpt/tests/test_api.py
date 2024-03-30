from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.response import Response
import pytest


@pytest.mark.django_db
def test_call_model(api_client_auth: APIClient) -> None:
    """
    Test success call_model API endpoint
    :param api_client_auth: APiClient
    :return: None
    """
    response: Response = api_client_auth.post(
        '/api/v1/call_model/',
        data = { 'prompt': 'hello' },
        format = 'json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content_type == 'application/json'
    assert response.data['response'] == 'dummy response from prompt: hello'


def test_call_model_without_auth(api_client: APIClient) -> None:
    """
    Test fail call_model API endpoint without authentication
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
def test_call_model_without_params(api_client_auth: APIClient) -> None:
    """
    Test fail call_model API endpoint without payload
    :param api_client_auth: APiClient
    :return: None
    """
    response: Response = api_client_auth.post(
        '/api/v1/call_model/',
        format = 'json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_call_model_without_wrong_params(api_client_auth: APIClient) -> None:
    """
    Test fail call_model API endpoint with wrong params
    :param api_client_auth: APiClient
    :return: None
    """
    response: Response = api_client_auth.post(
        '/api/v1/call_model/',
        data = { 'foo': 'hello' },
        format = 'json',
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


@pytest.mark.django_db
def test_call_async_model(api_client_auth: APIClient, mock_mljob) -> None:
    """
    Test success async_call_model API endpoint
    :param api_client_auth: APiClient
    :param mock_mljob: Create mock mljob
    :return: None
    """
    response: Response = api_client_auth.post(
        '/api/v1/async_call_model/',
        data = { 'prompt': 'hello' },
        format = 'json',
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.content_type == 'application/json'
    assert response.data['job_id'] == 123


def test_async_call_model_without_auth(api_client: APIClient, mock_mljob) -> None:
    """
    Test fail async_call_model API endpoint without authentication
    :param api_client: APiClient
    :param mock_mljob: Create mock mljob
    :return: None
    """
    response: Response = api_client.post(
        '/api/v1/async_call_model/',
        data = { 'prompt': 'hello' },
        format = 'json',
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
