from django.db import models

from npf.contrib.subject.models import AbstractSubject
from npf.core.modelaudit.models import AuditFieldsMixin


class Account(AuditFieldsMixin, models.Model):

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счета'

    class State:
        RESERVE = 'r'
        OPEN = 'o'
        CLOSE = 'c'
        FROZEN = 'f'
        CHOICES = (
            (RESERVE, 'Зарезевирован'),
            (OPEN, 'Открыт'),
            (CLOSE, 'Закрыт'),
            (FROZEN, 'Заморожен'),
        )

    class Type:
        CUMULATIVE = 'c'
        PAYMASTER = 'p'
        TRANSIT = 't'
        SOLIDARY = 's'
        CHOICES = (
            (CUMULATIVE, 'Накопительный'),
            (PAYMASTER, 'Выплатной'),
            (TRANSIT, 'Транзитный'),
            (SOLIDARY, 'Солидарный')
        )

    number = models.CharField(verbose_name='РН', max_length=255, unique=True)
    investor = models.ForeignKey(AbstractSubject, verbose_name='Вкладчик', related_name='participant_accounts')
    participant = models.ForeignKey(AbstractSubject, verbose_name='Участник', related_name="investor_accounts")

    transfer_rights_date = models.DateField(
        verbose_name='Дата перехода прав участнику',
        help_text='Дата перехода прав участнику на средства, учтенные на пенсионном счете, открытом на его имя.',
        blank=True,
        null=True
    )

    opened_at = models.DateTimeField(verbose_name='Дата и время открытия', blank=True, null=True)
    closed_at = models.DateTimeField(verbose_name='Дата и время закрытия', blank=True, null=True)
    state = models.CharField(verbose_name='Статус', max_length=1, choices=State.CHOICES, db_index=True)
    type = models.CharField(verbose_name='Тип', max_length=1, choices=Type.CHOICES, db_index=True)

    def __str__(self):
        return self.number

    @property
    def investor_and_participant_alike(self):
        return self.participant_id == self.investor_id