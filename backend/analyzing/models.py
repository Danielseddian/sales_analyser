from django.db import models

import uuid
from django.db import models

__all__ = ['SalesData', ]


class SalesData(models.Model):
    uuid = models.UUIDField(
        verbose_name='UUID', default=uuid.uuid4, unique=True, editable=False, primary_key=True, db_index=True,
    )
    xml_content = models.TextField(
        verbose_name='XML content',
    )
    report = models.JSONField(
        verbose_name='AI-based Report', null=True, blank=True,
    )
    reported_at = models.DateTimeField(
        verbose_name='Reported at', null=True, blank=True,
    )
    errors_log = models.JSONField(
        verbose_name='AI-response errors', null=True, blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name='User requested at', auto_now_add=True,
    )

    class Meta:
        verbose_name = 'sales data'
        verbose_name_plural = 'sales data'
