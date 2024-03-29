from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework import status, generics, serializers
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter, extend_schema, OpenApiExample, inline_serializer

from chatgpt.ml_model import super_chat_gpt_like_model


class ModelView(generics.GenericAPIView):

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
        data = JSONParser().parse(request)

        if 'prompt' not in data:
            return Response(status = status.HTTP_400_BAD_REQUEST)

        res = super_chat_gpt_like_model(data['prompt'])
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
