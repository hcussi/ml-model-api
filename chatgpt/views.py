from typing import Text
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from drf_spectacular.utils import extend_schema

from chatgpt.ml_model import super_chat_gpt_like_model
from chatgpt.models import MlModel, MlJob
from chatgpt.openapi import CALL_MODEL, ASYNC_CALL_MODEL, ASYNC_CALL_STATUS
from chatgpt.producers import ProducerMlPromptCreated
from chatgpt.decorators import rate_limited

producerMlPromptCreated = ProducerMlPromptCreated()
ML_MODEL_RATE_LIMIT = 3


class AuthenticateView(generics.GenericAPIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = (IsAuthenticated,)


class ModelView(AuthenticateView):

    @csrf_exempt
    @extend_schema(**CALL_MODEL)
    @rate_limited(rate_limit = ML_MODEL_RATE_LIMIT)
    def post(self, request: Request) -> Response:
        """
        Call the ChatGPT model and build the response
        :param request: Request
        :return: the response
        """
        start_time: datetime = timezone.now()

        data = JSONParser().parse(request)

        if 'prompt' not in data:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        prompt: Text = data['prompt']
        res = super_chat_gpt_like_model(data['prompt'])

        end_time: datetime = timezone.now()

        duration: timedelta = (end_time - start_time)

        MlModel(
            user_id=request.user.id,
            prompt=prompt,
            response=res,
            duration=duration,  # duration.total_seconds() * 10 ** 3  # ms
        ).save()

        return Response(
            { 'response': res },
            status = status.HTTP_201_CREATED,
            content_type = 'application/json',
        )


class HealthView(generics.GenericAPIView):

    @csrf_exempt
    @extend_schema(operation_id = 'health', description = 'Call the health endpoint')
    def get(self, _) -> Response:

        """
        Call the health endpoint and build the response
        :param _: ignored
        :return: the response
        """
        return Response(status = status.HTTP_204_NO_CONTENT)


class AsyncModelView(AuthenticateView):

    @csrf_exempt
    @extend_schema(**ASYNC_CALL_MODEL)
    @rate_limited(rate_limit = ML_MODEL_RATE_LIMIT)
    def post(self, request: Request) -> Response:
        """
        Call the ChatGPT model async and build the response
        :param request: Request
        :return: the response with the job id
        """
        start_time: datetime = timezone.now()

        data = JSONParser().parse(request)

        if 'prompt' not in data:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        prompt: Text = data['prompt']

        job = MlJob.objects.create(
            user_id=request.user.id,
            prompt=prompt,
            start_time=start_time,
        )

        producerMlPromptCreated.publish(job)

        return Response(
            { 'job_id': job.id },
            status = status.HTTP_200_OK,
            content_type = 'application/json',
        )


class AsyncModelStatusView(AuthenticateView):

    @csrf_exempt
    @extend_schema(**ASYNC_CALL_STATUS)
    def get(self, request, job_id: int) -> Response:
        """
        Returns the job status and the response if there is any
        :param request: Request
        :param job_id: The job id
        :return: the response with the job status
        """

        try:
            job = MlJob.objects.get(pk=job_id)
            mlmodel = getattr(job, 'mlmodel')
        except MlJob.DoesNotExist:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        if job.user.id != request.user.id:
            return Response(
                status = status.HTTP_403_FORBIDDEN,
            )

        return Response(
            { 'job_status': job.status, 'response': getattr(mlmodel, 'response', None) },
            status = status.HTTP_200_OK,
            content_type = 'application/json',
        )
