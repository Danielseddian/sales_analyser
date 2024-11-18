from xml.etree import ElementTree as ET
from asgiref.sync import async_to_sync, sync_to_async

from rest_framework import serializers
from adrf.serializers import Serializer as AsyncSerializer

from analyzing.models import SalesData
from management.wrappers.safe_execute import safe_execute, logger

__all__ = ['SalesDataSerializer']


class SalesDataSerializer(AsyncSerializer):
    xml_file = serializers.FileField(write_only=True)

    class Meta:
        fields = ['xml_file']

    @staticmethod
    async def validate_xml_file(value):
        try:
            value.open()
            xml_content = value.read()
            xml_content = xml_content.decode('utf-8')

            root = ET.fromstring(xml_content)
            if root.tag != 'sales_data' or 'date' not in root.attrib:
                raise serializers.ValidationError('Неправильная структура XML.')
            for product in root.findall('./products/product'):
                if not all(child.tag in {'id', 'name', 'quantity', 'price', 'category'} for child in product):
                    raise serializers.ValidationError('Неправильная структура продукта XML.')
            return xml_content
        except ET.ParseError:
            raise serializers.ValidationError('Невозможно разобрать XML файл.')
        except Exception as error:
            logger.exception(f'XML parsing error: {error}.', exc_info=error)
        finally:
            value.close()

    @safe_execute()
    async def asave(self, **kwargs):
        return await SalesData.objects.acreate(xml_content=await self.validated_data['xml_file'])
