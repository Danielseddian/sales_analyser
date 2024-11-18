import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings
from rest_framework.exceptions import ValidationError

from analyzing.serializers import SalesDataSerializer


@pytest.mark.asyncio
class TestSalesDataSerializer:
    @staticmethod
    def get_valid_xml():
        xml_content = b"""
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
        """
        return SimpleUploadedFile("sales_data.xml", xml_content, content_type="text/xml")

    @staticmethod
    def get_invalid_xml():
        xml_content = b"""
        <sales_data date="2024-01-01">
            <products>
                <product>
                    <id>1</id>
                    <name>Product 1</name>
                </product>
            </products>
        </sales_data>
        """
        return SimpleUploadedFile("invalid_data.xml", xml_content, content_type="text/xml")

    @staticmethod
    def get_corrupted_xml():
        xml_content = b"<sales_data><invalid></sales"
        return SimpleUploadedFile("corrupted_data.xml", xml_content, content_type="text/xml")

    async def test_validate_xml_file_success(self):
        serializer = SalesDataSerializer(data={'xml_file': self.get_valid_xml()})
        assert await serializer.async_is_valid(raise_exception=True)
        assert 'xml_file' in serializer.validated_data

    async def test_validate_xml_file_invalid_structure(self):
        serializer = SalesDataSerializer(data={'xml_file': self.get_invalid_xml()})
        with pytest.raises(ValidationError, match="Неправильная структура продукта XML"):
            await serializer.async_is_valid(raise_exception=True)

    async def test_validate_xml_file_corrupted(self):
        serializer = SalesDataSerializer(data={'xml_file': self.get_corrupted_xml()})
        with pytest.raises(ValidationError, match="Невозможно разобрать XML файл"):
            await serializer.async_is_valid(raise_exception=True)

    async def test_save_successful(self, mocker):
        # Mocking the SalesData model to avoid actual database interaction
        mock_sales_data = mocker.patch("analyzing.serializers.SalesData.objects.acreate")
        mock_sales_data.return_value = None  # Simulate a successful save

        serializer = SalesDataSerializer(data={'xml_file': self.get_valid_xml()})
        assert await serializer.async_is_valid(raise_exception=True)
        await serializer.asave()
        mock_sales_data.assert_called_once_with(xml_content=mocker.ANY)

    async def test_save_failure(self, mocker):
        mock_sales_data = mocker.patch("analyzing.models.SalesData.objects.acreate")
        mock_sales_data.side_effect = Exception("Database error")

        serializer = SalesDataSerializer(data={'xml_file': self.get_valid_xml()})
        assert await serializer.async_is_valid(raise_exception=True)

        with override_settings(SAFE_EXECUTE=False):
            with pytest.raises(Exception, match="Database error"):
                await serializer.asave()
