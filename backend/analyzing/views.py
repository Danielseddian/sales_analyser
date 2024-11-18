from adrf.views import APIView as AsyncApiView
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from analyzing.models import SalesData
from analyzing.serializers import SalesDataSerializer
from analyzing.tasks import analyze_sales_data
from management.wrappers.safe_execute import safe_execute

__all__ = ['SalesDataUploadView', 'GetSalesDataResultView']

User = get_user_model()


class SalesDataUploadView(AsyncApiView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        request_body=SalesDataSerializer,
        responses={
            status.HTTP_202_ACCEPTED: openapi.Response(
                description='Файл успешно загружен',
                examples={
                    'application/json': {
                        'message': 'Запрос на анализ принят.',
                        'uuid': '123e4567-e89b-12d3-a456-426614174000',
                        'result_url': '/api/v1/analyzing/result/123e4567-e89b-12d3-a456-426614174000/',
                    }
                },
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description='Ошибка: Неверная структура XML',
                examples={'application/json': {'detail': 'Неверная структура XML.'}},
            ),
        }
    )
    def post(self, request, *args, **kwargs):
        return async_to_sync(self.apost)(request, *args, **kwargs)

    async def apost(self, request, *args, **kwargs):
        serializer = SalesDataSerializer(data=request.data)
        if await serializer.async_is_valid(raise_exception=True):
            sales_data = await serializer.asave()
            await analyze_sales_data.delay(sales_data.uuid)  # Sending data for analysis
            url = request.build_absolute_uri(reverse('api:analyzing:get-sales-data-result', args=[sales_data.uuid]))
            return Response(
                {
                    'message': 'Запрос на анализ принят.',
                    'uuid': sales_data.uuid,
                    'result_url': url
                },
                status=status.HTTP_202_ACCEPTED,
            )
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class GetSalesDataResultView(AsyncApiView):
    permission_classes = [AllowAny]
    view_is_async = True

    @swagger_auto_schema(
        operation_description='Получить результат анализа данных о продажах по UUID',
        responses={
            status.HTTP_200_OK: openapi.Response(
                description='Результат анализа',
                examples={
                    'application/json': {
                        'report': {
                            'date': '2024-01-01',
                            'total_revenue': 150000,
                            'top_products': [
                                {'id': 1, 'name': 'Product A', 'quantity': 100},
                                {'id': 2, 'name': 'Product B', 'quantity': 75},
                                {'id': 3, 'name': 'Product C', 'quantity': 50},
                            ],
                            'categories': {
                                'Electronics': 150000,
                                'Clothing': 50000,
                            },
                            'analysis_summary': (
                                'Electronics dominated sales. Consider increasing stock for high-demand products.'
                            )
                        }
                    }
                },
            ),
            status.HTTP_202_ACCEPTED: openapi.Response(
                description='Отчёт ещё формируется',
                examples={
                    'application/json': {
                        'message': (
                            'Запрос получен 2024-11-12. Отчёт ещё формируется. Получить его можно будет немного позже.'
                        )
                    }
                },
            ),
            status.HTTP_204_NO_CONTENT: openapi.Response(
                description='Ошибка формирования отчёта',
                examples={'application/json': {'detail': 'Не удалось сформировать отчёт.'}},
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description='Данные с указанным UUID не найдены',
                examples={
                    'application/json': {
                        'detail': 'Запрашиваемый объект `123e4567-e89b-12d3-a456-426614174000` не найден.'
                    },
                },
            ),
        },
    )
    @safe_execute(Response, data={'message': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request, uuid, *args, **kwargs):
        return async_to_sync(self.aget)(request, uuid, *args, **kwargs)

    async def aget(self, request, uuid, *args, **kwargs):
        try:
            sales_data = await SalesData.objects.aget(uuid=uuid)
        except SalesData.DoesNotExist:
            return Response({'detail': f'Запрашиваемый объект `{uuid}` не найден.'}, status=status.HTTP_404_NOT_FOUND)
        if sales_data.errors_log:
            return Response({'detail': sales_data.errors_log}, status=status.HTTP_204_NO_CONTENT)
        if not sales_data.reported_at:
            return Response(
                {
                    'message': (
                        f'Запрос получен {sales_data.created_at}. Отчёт ещё формируется.'
                        f' Получить его можно будет немного позже.'
                    )
                },
                status=status.HTTP_202_ACCEPTED,
            )
        return Response({'report': sales_data.report}, status=status.HTTP_200_OK)
