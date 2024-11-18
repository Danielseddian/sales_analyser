import asyncio
from xml.etree import ElementTree as ET

from rest_framework import serializers
from adrf.serializers import Serializer as AsyncSerializer
from rest_framework.exceptions import ValidationError

from analyzing.models import SalesData
from management.wrappers.safe_execute import safe_execute, logger

__all__ = ['SalesDataSerializer']


class SalesDataSerializer(AsyncSerializer):
    xml_file = serializers.FileField(write_only=True)

    class Meta:
        fields = ['xml_file']

    async def async_is_valid(self, *, raise_exception=False):
        super().is_valid(raise_exception=False)
        for field in SalesDataSerializer.Meta.fields:
            field_ = self.validated_data.get(field)
            if asyncio.iscoroutine(field_):
                try:
                    self.validated_data[field] = await field_
                except ValidationError as error:
                    self._errors[field] = error.detail[0]
        if self._errors and raise_exception:
            raise ValidationError(self._errors)
        return not bool(self._errors)

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
                if sorted([child.tag for child in product]) != sorted({'id', 'name', 'quantity', 'price', 'category'}):
                    raise serializers.ValidationError('Неправильная структура продукта XML.')
            return xml_content
        except ET.ParseError:
            raise serializers.ValidationError('Невозможно разобрать XML файл.')
        finally:
            value.close()

    @safe_execute()
    async def asave(self, **kwargs):
        return await SalesData.objects.acreate(xml_content=self.validated_data['xml_file'])
