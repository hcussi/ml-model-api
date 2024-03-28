from django.urls import path

from . import views

urlpatterns = [
    path('call_model/', views.index, name='prompt'),
]
