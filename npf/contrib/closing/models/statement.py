from django.db import models

from npf.core.modelaudit.models import AuditFieldsMixin
from npf.contrib.subject.models import Person


class Statement(AuditFieldsMixin, models.Model):
    number = models.CharField(max_length=255, verbose_name='Номер документа', null=True, blank=True)

    person = models.ForeignKey(Person)
    bank = models.CharField(max_length=255, verbose_name='Наименование банка получателя', null=True, blank=True)
    bank_otdel = models.CharField(max_length=255, verbose_name='Наименование отделения банка', null=True, blank=True)
    number_otdel = models.CharField(max_length=255, verbose_name='№ отделения / № филиала (доп. офиса)', null=True, blank=True)
    inn = models.CharField(max_length=255, verbose_name='ИНН', null=True, blank=True)
    rs = models.CharField(max_length=255, verbose_name='Расчетный счет отделения', null=True, blank=True)
    kr = models.CharField(max_length=255, verbose_name='Корреспондентский счет отделения', null=True, blank=True)
    bik = models.CharField(max_length=255, verbose_name='БИК', null=True, blank=True)
    ls = models.CharField(max_length=255, verbose_name='Лицевой счет', null=True, blank=True)
    t = models.NullBooleanField(default=False, verbose_name='Прилагается справка о социальнм налоговом вачете', null=True, blank=True)

    status = models.CharField(max_length=255, verbose_name='Статус', null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'Заявление'
        verbose_name_plural = 'Заявления'