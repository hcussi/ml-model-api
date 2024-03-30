from rest_framework import serializers
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter, OpenApiExample, inline_serializer

CALL_MODEL = {
    'operation_id': 'call_model',
    'description': 'Call the ChatGPT model and return the text response',
    'parameters': [
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
    'responses': {
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
    'examples': [
        OpenApiExample(
            'Example of call_model response.',
            value = { 'response': 'dummy response from prompt: hello' },
            request_only = False,
            response_only = True,
        ),
    ],
}

ASYNC_CALL_MODEL = {
    'operation_id': 'async_call_model',
    'description': 'Async call the ChatGPT model and return the job id',
    'parameters': [
        OpenApiParameter(
            name = 'payload',
            description = 'Prompt text',
            type = inline_serializer(name = 'async-prompt-payload', fields = { 'prompt': serializers.CharField() }),
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
    'responses': {
        201: OpenApiResponse(
            response = inline_serializer(
                name = 'async-prompt-response',
                fields = { 'job_id': serializers.IntegerField() },
            ),
            description = 'Created. Job now is schedule to run soon'
        ),
        400: OpenApiResponse(description = 'Bad request'),
        401: OpenApiResponse(description = 'Unauthorized'),
    },
    'examples': [
        OpenApiExample(
            'Example of async_call_model response.',
            value = { 'job_id': 123 },
            request_only = False,
            response_only = True,
        ),
    ],
}

ASYNC_CALL_STATUS = {
    'operation_id': 'async_call_status',
    'description': 'Return the job status and response if there is any',
    'responses': {
        200: OpenApiResponse(
            response = inline_serializer(
                name = 'status-response',
                fields = { 'job_status': serializers.CharField(), 'response': serializers.CharField() },
            ),
            description = 'The job status and the response if there is any'
            ),
        400: OpenApiResponse(description = 'Bad request'),
        401: OpenApiResponse(description = 'Unauthorized'),
    },
    'examples': [
        OpenApiExample(
            'Example of async_call_status pending job.',
            value = { 'job_status': 'pending', 'response': None },
            request_only = False,
            response_only = True,
        ),
        OpenApiExample(
            'Example of async_call_status done job.',
            value = { 'job_status': 'done', 'response': 'dummy response from prompt: hello' },
            request_only = False,
            response_only = True,
        ),
    ],
}
