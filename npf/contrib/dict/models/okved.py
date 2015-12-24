from django.db import models

from npf.core.xmin.models import XminTreeModel


class OKVED(XminTreeModel):
    code = models.CharField(verbose_name='Код', max_length=9)
    name = models.TextField(verbose_name='Наименование')

    class Meta:
        verbose_name = 'ОКВЭД'
        verbose_name_plural = 'ОКВЭД'

    def __str__(self):
        return '{0} {1}'.format(self.code, self.name)