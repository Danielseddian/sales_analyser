import openai

from celery import shared_task

from django.utils import timezone
from django.conf import settings

from analyzing.models import SalesData
from analyzing.tools import parse_xml
from management.wrappers.safe_execute import safe_execute

__all__ = ['analyze_sales_data']


@shared_task
@safe_execute()
def analyze_sales_data(sales_data_uuid):
    sales_data = SalesData.objects.get(uuid=sales_data_uuid)
    try:
        parsed_data = parse_xml(sales_data.xml_content)
        example = {
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
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            messages=[
                {
                    'role': 'user',
                    'content': (
                        f'Analyze the sales data for {parsed_data["date"]}: {parsed_data["products"]}. '
                        f'Return result with recommendations in JSON format like: {example}.'
                    ),
                },
            ],
            model='gpt-4o-mini',
        )
        sales_data.report = response['choices'][0]['message']['content']
    except Exception as error:
        sales_data.errors_log = str(error)
    sales_data.reported_at = timezone.now()
    sales_data.save()
