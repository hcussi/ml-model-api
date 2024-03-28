from django.urls import path

from . import views

urlpatterns = [
    path('call_model/<str:prompt>', views.index, name='prompt'),
]
