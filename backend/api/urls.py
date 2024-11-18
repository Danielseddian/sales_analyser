from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import schema_view

app_name = 'api'

router = DefaultRouter()

urlpatterns = [
    path('analyzing/', include('analyzing.urls', namespace='analyzing')),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
]

urlpatterns += router.urls
