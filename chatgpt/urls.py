from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from chatgpt.views import ModelView, HealthView, AsyncModelView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('call_model/', ModelView.as_view(), name='call-model'),
    path('async_call_model/', AsyncModelView.as_view(), name='async-call-model'),
    path('health/', HealthView.as_view(), name='health'),
]
