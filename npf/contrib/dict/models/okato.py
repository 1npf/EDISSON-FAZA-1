from django.db import models

from npf.core.xmin.models import XminTreeModel


class OKATO(XminTreeModel):
    code = models.CharField(verbose_name='Код', unique=True, max_length=11)
    name = models.CharField(verbose_name='Наименование', max_length=255)
    additional_info = models.CharField(verbose_name='Дополнительная информация', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = 'ОКАТО'
        verbose_name_plural = 'ОКАТО'

    def __str__(self):
        return '{0} {1}'.format(self.code, self.name)