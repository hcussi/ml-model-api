from django.http import HttpResponse

from chatgpt.ml_model import super_chat_gpt_like_model


def index(_, prompt: str):
    res = super_chat_gpt_like_model(prompt)
    return HttpResponse(res)
