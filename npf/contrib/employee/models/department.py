from django.db import models

from npf.core.xmin.models import XminTreeModel


class Department(XminTreeModel):
    name = models.CharField(verbose_name='Название', max_length=255)

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        db_table = 'employee_department'

    def __str__(self):
        return self.name