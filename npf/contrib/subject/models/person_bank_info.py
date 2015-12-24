from django.db import models

from npf.contrib.subject.models import Person


class PersonBankInfo(models.Model):

    class Meta:
        verbose_name = 'Банковские реквизиты'
        verbose_name_plural = 'Банковские реквизиты'
        db_table = 'subject_bank_info'

    person = models.OneToOneField(Person, parent_link=True, primary_key=True)
    account = models.CharField(verbose_name="Номер счёта", max_length=255)
    bank = models.ForeignKey(to='dict.Bank', verbose_name='Банк', blank=True, null=True)