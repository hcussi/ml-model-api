from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from chatgpt.ml_model import super_chat_gpt_like_model


@api_view(['POST'])
@csrf_exempt
def index(request: Request) -> Response:
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
        {'response': res},
        status=status.HTTP_201_CREATED,
        content_type = 'application/json',
    )


@api_view(['GET'])
@csrf_exempt
def health(_) -> Response:
    """
    Call the health endpoint and build the response
    :param _: ignored
    :return: the response
    """
    return Response(status=status.HTTP_204_NO_CONTENT)
