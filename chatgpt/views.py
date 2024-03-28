from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from chatgpt.ml_model import super_chat_gpt_like_model


@api_view(['POST'])
def index(request):
    data = JSONParser().parse(request)
    res = super_chat_gpt_like_model(data['prompt'])
    return Response(
        {'response': res},
        status=status.HTTP_201_CREATED,
    )
