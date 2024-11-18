from drf_yasg.views import get_schema_view
from drf_yasg import openapi

__all__ = ['schema_view']

from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Sales Data API",
        default_version='v1',
        description="API для анализа данных о продажах",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)
