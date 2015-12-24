from django.db import models

from npf.core.modelaudit.models import AuditFieldsMixin


class IdentityDocumentMixin(AuditFieldsMixin, models.Model):

    class Meta:
        abstract = True

    series = models.CharField(verbose_name='Серия', max_length=255)
    number = models.CharField(verbose_name='Номер', max_length=255)
    issue_date = models.DateField(verbose_name='Дата выдачи')
    issued_by = models.CharField(verbose_name='Кем выдан', max_length=255)
    original = models.FileField(verbose_name='Оригинал', null=True, blank=True)

    def __str__(self):
        return '{0} {1}'.format(self.series, self.number)