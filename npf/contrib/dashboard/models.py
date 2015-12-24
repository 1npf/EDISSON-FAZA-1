from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType


class Bookmark(models.Model):
    content_type = models.ForeignKey(verbose_name='Тип содержимого', to=ContentType)
    user = models.ForeignKey(verbose_name='Пользователь', to=settings.AUTH_USER_MODEL)
    record_id = models.BigIntegerField(verbose_name='ИД записи', null=True, blank=True)

    class Meta:
        verbose_name = 'Закладка'
        verbose_name_plural = 'Закладки'

    def __str__(self):
        model = self.content_type.model_class()
        if not model:
            return super().__str__()
        if self.record_id:
            return '{0}: {1}'.format(model._meta.verbose_name, self.record_id)
        return str(model._meta.verbose_name_plural)