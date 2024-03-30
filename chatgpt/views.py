from typing import Text
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter, extend_schema, OpenApiExample, inline_serializer

from chatgpt.ml_model import super_chat_gpt_like_model
from chatgpt.models import MlModel, MlJob


class ModelView(generics.GenericAPIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    @extend_schema(
        operation_id = 'call_model',
        description = 'Call the ChatGPT model and return the text response',
        parameters = [
            OpenApiParameter(
                name = 'payload',
                description = 'Prompt text',
                type = inline_serializer(name = 'prompt-payload', fields = { 'prompt': serializers.CharField() }),
                examples = [
                    OpenApiExample(
                        'Example of call_model request.',
                        value = { 'prompt': 'hello' },
                        request_only = True,
                        response_only = False,
                    ),
                ],
            ),
        ],
        responses = {
            201: OpenApiResponse(
                response = inline_serializer(
                    name = 'prompt-response',
                    fields = { 'response': serializers.CharField() },
                ),
                description = 'Created. New resource in response'
                ),
            400: OpenApiResponse(description = 'Bad request'),
            401: OpenApiResponse(description = 'Unauthorized'),
        },
        examples = [
            OpenApiExample(
                'Example of call_model response.',
                value = { 'response': 'dummy response from prompt: hello' },
                request_only = False,
                response_only = True,
            ),
        ],
    )
    def post(self, request: Request) -> Response:
        """
        Call the ChatGPT model and build the response
        :param request: Request
        :return: the response
        """
        start_time: datetime = datetime.now()

        data = JSONParser().parse(request)

        if 'prompt' not in data:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        prompt: Text = data['prompt']
        res = super_chat_gpt_like_model(data['prompt'])

        end_time: datetime = datetime.now()

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
    @extend_schema(
        operation_id = 'health',
        description = 'Call the health endpoint',
    )
    def get(self, _) -> Response:

        """
        Call the health endpoint and build the response
        :param _: ignored
        :return: the response
        """
        return Response(status = status.HTTP_204_NO_CONTENT)


class AsyncModelView(generics.GenericAPIView):

    authentication_classes = [BasicAuthentication]
    permission_classes = (IsAuthenticated,)

    @csrf_exempt
    @extend_schema(
        operation_id = 'async_call_model',
        description = 'Async call the ChatGPT model and return the job id',
        parameters = [
            OpenApiParameter(
                name = 'payload',
                description = 'Prompt text',
                type = inline_serializer(name = 'prompt-payload', fields = { 'prompt': serializers.CharField() }),
                examples = [
                    OpenApiExample(
                        'Example of async_call_model request.',
                        value = { 'prompt': 'hello' },
                        request_only = True,
                        response_only = False,
                    ),
                ],
            ),
        ],
        responses = {
            201: OpenApiResponse(
                response = inline_serializer(
                    name = 'prompt-response',
                    fields = { 'job_id': serializers.IntegerField() },
                ),
                description = 'Created. Job now is schedule to run soon'
                ),
            400: OpenApiResponse(description = 'Bad request'),
            401: OpenApiResponse(description = 'Unauthorized'),
        },
        examples = [
            OpenApiExample(
                'Example of async_call_model response.',
                value = { 'job_id': 123 },
                request_only = False,
                response_only = True,
            ),
        ],
    )
    def post(self, request: Request) -> Response:
        """
        Call the ChatGPT model async and build the response
        :param request: Request
        :return: the response with the job id
        """
        start_time: datetime = datetime.now()

        data = JSONParser().parse(request)

        if 'prompt' not in data:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        prompt: Text = data['prompt']

        # async code

        job = MlJob.objects.create(
            user_id=request.user.id,
            prompt=prompt,
            start_time=start_time,
        )

        # end async code

        return Response(
            { 'job_id': job.id },
            status = status.HTTP_200_OK,
            content_type = 'application/json',
        )
