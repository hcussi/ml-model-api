from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.response import Response
import pytest
from django.contrib.auth.models import User
from rest_framework import HTTP_HEADER_ENCODING
import base64

from chatgpt.models import MlJobStatus, MlJob


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
def test_async_call_model(api_client_auth: APIClient, mock_mljob: None, mock_mlprompt_producer: None) -> None:
    """
    Test success async_call_model API endpoint
    :param api_client_auth: APiClient
    :param mock_mljob: Create mock mljob
    :param mock_mlprompt_producer: Create mock producer
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


@pytest.mark.django_db
def test_async_call_status_pending(api_client_auth: APIClient, mljob_pending: MlJob) -> None:
    """
    Test success async_call_status API endpoint
    :param api_client_auth: APiClient
    :param mljob_pending: Create mljob
    :return: None
    """
    response: Response = api_client_auth.get(f'/api/v1/async_call_status/{mljob_pending.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.content_type == 'application/json'
    assert response.data['job_status'] == MlJobStatus.PENDING
    assert response.data['response'] is None


@pytest.mark.django_db
def test_async_call_status_done(api_client_auth: APIClient, mljob_done: MlJob) -> None:
    """
    Test success async_call_status API endpoint
    :param api_client_auth: APiClient
    :param mljob_done: Create mljob
    :return: None
    """
    response: Response = api_client_auth.get(f'/api/v1/async_call_status/{mljob_done.id}')
    assert response.status_code == status.HTTP_200_OK
    assert response.content_type == 'application/json'
    assert response.data['job_status'] == MlJobStatus.DONE
    assert response.data['response'] == 'dummy response from prompt: hello'


@pytest.mark.django_db
def test_async_call_status_unexisting_job(api_client_auth: APIClient) -> None:
    """
    Test fail async_call_status API endpoint with unexisting job
    :param api_client_auth: APiClient
    :return: None
    """
    response: Response = api_client_auth.get('/api/v1/async_call_status/123')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_async_call_status_forbidden(api_client: APIClient, mljob_done: MlJob, another_user: User) -> None:
    """
    Test fail async_call_status API endpoint with different user
    :param api_client: APiClient
    :param mljob_done: Create mljob
    :param another_user: Create another user
    :return: None
    """
    base64_credentials = base64.b64encode('test2:secret1234'.encode(HTTP_HEADER_ENCODING)).decode(HTTP_HEADER_ENCODING)
    api_client.credentials(HTTP_AUTHORIZATION = 'Basic %s' % base64_credentials)

    response: Response = api_client.get(f'/api/v1/async_call_status/{mljob_done.id}')
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_async_call_status_without_auth(api_client: APIClient, mljob_pending: MlJob) -> None:
    """
    Test fail async_call_status API endpoint without auth
    :param api_client: APiClient
    :param mljob_pending: Create mljob
    :return: None
    """
    response: Response = api_client.get(f'/api/v1/async_call_status/{mljob_pending.id}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_call_model_rate_limit(api_client_auth: APIClient, multiple_mlmodels: None) -> None:
    """
    Test fail call_model API endpoint for rate limit
    :param api_client_auth: APiClient
    :param multiple_mlmodels: Create multiple ml models
    :return: None
    """
    response: Response = api_client_auth.post(
        '/api/v1/call_model/',
        data = { 'prompt': 'hello' },
        format = 'json',
    )
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS


@pytest.mark.django_db
def test_async_call_model_rate_limit(api_client_auth: APIClient, multiple_mlmodels: None) -> None:
    """
    Test fail async_call_model API endpoint for rate limit
    :param api_client_auth: APiClient
    :param multiple_mlmodels: Create multiple ml models
    :return: None
    """
    response: Response = api_client_auth.post(
        '/api/v1/async_call_model/',
        data = { 'prompt': 'hello' },
        format = 'json',
    )
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
