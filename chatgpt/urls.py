from django.urls import path

from . import views

urlpatterns = [
    path('call_model/', views.index, name='call-model'),
    path('health/', views.health, name='health'),
]
