from django.db import models

from npf.core.xmin.models import XminTreeModel


class Bank(XminTreeModel):
    name = models.TextField(verbose_name='Банк')
    bik = models.CharField(verbose_name='БИК', max_length=9)

    class Meta:
        verbose_name = 'Банк'
        verbose_name_plural = 'Банки'
        db_table = 'dict_bank'

    def __str__(self):
        return '{0} {1}'.format(self.bik, self.name)