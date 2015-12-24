from django.db import models

from npf.core.modelaudit.models import AuditFieldsMixin
from npf.contrib.account.models import Account


class Contract(AuditFieldsMixin, models.Model):

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Список договоров'

    class State:
        CONCLUDED = 'concluded'
        COMPLETED = 'completed'
        TERMINATION = 'termination'
        TERMINATED = 'terminated'
        CHOICES = (
            (CONCLUDED, 'Заключен'),
            (COMPLETED, 'Исполнен'),
            (TERMINATION, 'На стадии расторжения'),
            (TERMINATED, 'Расторгнут'),
        )

    class ContributionPeriod:
        MONTH = 'm'
        QUARTER = 'q'
        YEAR = 'y'
        CHOICES = (
            (MONTH, 'Ежемесячно'),
            (QUARTER, 'Ежеквартально'),
            (YEAR, 'Ежегодно'),
        )

    account = models.OneToOneField(verbose_name='РН', to=Account)
    conclusion_date = models.DateField(verbose_name='Дата заключения')
    termination_date = models.DateField(verbose_name='Дата расторжения', blank=True, null=True)
    state = models.CharField(verbose_name='Статус', max_length=11, choices=State.CHOICES, db_index=True)