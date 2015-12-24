from django.db import models

from npf.contrib.account.models import Contract
from npf.contrib.dict import models as dicts


class ContractPersonNpo(Contract):

    class Meta:
        verbose_name = 'Договор с ФЛ в свою пользу (НПО)'
        verbose_name_plural = 'Реестр договоров с ФЛ в свою пользу (НПО)'
        db_table = 'account_contract_person_npo'

    start_payment_date = models.DateField(verbose_name='Дата начала пенсионных взосов')
    end_payment_date = models.DateField(verbose_name='Дата окончания пенсионных взносов')
    contribution_period = models.CharField(verbose_name='Переодичность взносов', max_length=1,
                                           choices=Contract.ContributionPeriod.CHOICES, db_index=True)

    regular_payment_percent = models.IntegerField(verbose_name='Размер регулярного взноса (% от МРОТ)', default=10)
    pension_scheme = models.ForeignKey(to=dicts.PensionScheme, verbose_name='Пенсионная схема')

    def __str__(self):
        return self.account.number