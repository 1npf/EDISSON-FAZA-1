from django.db import models

from npf.contrib.subject.models import AbstractSubject


class PensionFund(AbstractSubject):

    class Meta:
        verbose_name = 'Пенсионный фонд'
        verbose_name_plural = 'Пенсионный фонд России и другие НПФ'
        db_table = 'subject_pension_fund'

    management_company = models.BooleanField(verbose_name='Наличие управляющей компании', default=False)
    notes = models.TextField(verbose_name='Примечания', blank=True, null=True)
    license = models.CharField(verbose_name='Номер лицензии', max_length=255, blank=True, null=True)
    license_issue_date = models.DateField(verbose_name='Дата выдачи лицензии', blank=True, null=True)
    legal_form = models.ForeignKey(to='dict.LegalForm', verbose_name='ОПФ', blank=True, null=True)
    ovd = models.CharField(verbose_name='ОВД', max_length=255, blank=True, null=True)
    inn = models.CharField(verbose_name='ИНН', max_length=20, blank=True, null=True)
    okpo = models.CharField(verbose_name='ОКПО', max_length=20, blank=True, null=True)
    registration = models.TextField(verbose_name='Зарегистрирован (где и кем)', blank=True, null=True)
    phone = models.CharField(verbose_name='Телефоны', max_length=255, blank=True, null=True)
    fax = models.CharField(verbose_name='Факс', max_length=155, blank=True, null=True)
    region = models.CharField(verbose_name='Действует в регионе', max_length=255, blank=True, null=True)
    additional_information = models.TextField(verbose_name='Доп. информация', blank=True, null=True)
    postal_address = models.OneToOneField(verbose_name='Почтовый адрес', to='address.House', related_name='+')
    legal_address = models.OneToOneField(verbose_name='Юридический ардес', to='address.House', related_name='+')
    actual_address = models.OneToOneField(verbose_name='Фактический адрес', to='address.House', related_name='+')
    contacts = models.TextField(verbose_name='Контактные данные ключевых сотрудников', blank=True, null=True)

    def __str__(self):
        return self.name
