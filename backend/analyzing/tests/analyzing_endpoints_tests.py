import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from analyzing.models import SalesData
from uuid import uuid4


@pytest.mark.django_db
class TestSalesDataViews:

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def sales_data(self):
        return SalesData.objects.create(
            uuid=uuid4(),
            xml_content=b"""
                <sales_data date="2024-01-01">
                    <products>
                        <product>
                            <id>1</id>
                            <name>Product 1</name>
                            <quantity>10</quantity>
                            <price>99.99</price>
                            <category>Category 1</category>
                        </product>
                    </products>
                </sales_data>
                """,
        )

    def test_sales_data_incorrect_file_upload(self, client):
        url = reverse('api:analyzing:upload-sales-data')

        with open('dummy_file.xml', 'wb') as f:
            f.write(b"""
                <sales_data date="2024-01-01">
                    <products>
                        <product>test</product>
                    </products>
                </sales_data>
                """)

        with open('dummy_file.xml', 'rb') as f:
            response = client.post(url, {'xml_file': f}, format='multipart')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'xml_file' in response.data
        assert response.data['xml_file'] == 'Неправильная структура продукта XML.'

    def test_get_sales_data_result(self, client, sales_data):
        sales_data.reported_at = '2024-01-01T00:00:00Z'
        sales_data.report = '{"report": "test report"}'
        sales_data.save()
        url = reverse('api:analyzing:get-sales-data-result', kwargs={'uuid': sales_data.uuid})

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert 'report' in response.data
        assert 'test report' in response.data['report'] 

    def test_get_sales_data_result_not_found(self, client):
        url = reverse('api:analyzing:get-sales-data-result', kwargs={'uuid': uuid4()})

        response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'detail' in response.data

    def test_get_sales_data_result_in_progress(self, client, sales_data):
        sales_data.reported_at = None
        sales_data.save()

        url = reverse('api:analyzing:get-sales-data-result', kwargs={'uuid': sales_data.uuid})

        response = client.get(url)

        assert response.status_code == status.HTTP_202_ACCEPTED
        assert 'message' in response.data
        assert 'Отчёт ещё формируется' in response.data['message']

    def test_get_sales_data_result_with_error(self, client, sales_data):
        sales_data.errors_log = 'Error processing the file'
        sales_data.save()

        url = reverse('api:analyzing:get-sales-data-result', kwargs={'uuid': sales_data.uuid})

        response = client.get(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert 'detail' in response.data
        assert 'Error processing the file' in response.data['detail']