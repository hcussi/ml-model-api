from rest_framework import status
from rest_framework.test import APIClient


def test_call_model(api_client: APIClient) -> None:
    """
    Test success call_model API endpoint
    :param api_client: APiClient
    :return: None
    """
    response = api_client.post(
        '/api/v1/call_model/',
        data = { 'prompt': 'hello' },
        format = 'json',
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content_type == 'application/json'
    assert response.data['response'] == 'dummy response from prompt: hello'


def test_call_model_without_params(api_client: APIClient) -> None:
    """
    Test the update task API
    :param api_client: APiClient
    :return: None
    """
    response = api_client.post(
        '/api/v1/call_model/',
        format = 'json',
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_call_model_without_wrong_params(api_client: APIClient) -> None:
    """
    Test the update task API
    :param api_client: APiClient
    :return: None
    """
    response = api_client.post(
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
    response = api_client.get('/api/v1/health/')
    assert response.status_code == status.HTTP_204_NO_CONTENT
