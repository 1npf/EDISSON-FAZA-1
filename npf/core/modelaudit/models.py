from django.conf import settings
from django.db import models


class AuditFieldsMixin(models.Model):

    class Meta:
        abstract = True

    added_at = models.DateTimeField(verbose_name='Дата и время создания', auto_now_add=True, db_index=True)
    modified_at = models.DateTimeField(verbose_name='Дата и время модификации', auto_now=True, db_index=True)
    added_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Автор', related_name='+')
    modified_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Последние изменения осуществил',
                                         related_name='+')