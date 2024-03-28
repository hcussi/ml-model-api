from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from chatgpt.ml_model import super_chat_gpt_like_model


@api_view(['POST'])
@csrf_exempt
def index(request):
    data = JSONParser().parse(request)
    res = super_chat_gpt_like_model(data['prompt'])
    return Response(
        {'response': res},
        status=status.HTTP_201_CREATED,
    )


@api_view(['GET'])
@csrf_exempt
def health(_):
    return Response(status=status.HTTP_204_NO_CONTENT)
