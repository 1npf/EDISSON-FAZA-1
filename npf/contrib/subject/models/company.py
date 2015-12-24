from django.db import models

from npf.contrib.subject.models import AbstractSubject


class Company(AbstractSubject):

    class Meta:
        verbose_name = 'Юридическое лицо'
        verbose_name_plural = 'Вкладчики ЮЛ'

    legal_form = models.ForeignKey(to='dict.LegalForm', verbose_name='Правовая форма')
    short_name = models.CharField(verbose_name='Краткое наименование', max_length=255)
    full_name = models.CharField(verbose_name='Полное наименование', max_length=255, blank=True, null=True)
    second_name = models.CharField(verbose_name='Наименование на иностранном языке', max_length=255, blank=True,
                                   null=True)
    register_entry = models.CharField(verbose_name='Орган, зарегистрировавший ЮЛ', max_length=255,
                                      blank=True, null=True)
    register_number = models.CharField(verbose_name='Номер', max_length=255, blank=True, null=True)
    register_date = models.DateField(verbose_name='Дата', blank=True, null=True)
    ogrn = models.CharField(verbose_name='ОГРН', max_length=255, blank=True, null=True)
    inn = models.CharField(verbose_name='ИНН', max_length=255, blank=True, null=True)
    kpp = models.CharField(verbose_name='КПП', max_length=255, blank=True, null=True)
    okved = models.ForeignKey(verbose_name='ОКВЭД', to='dict.OKVED', blank=True, null=True)
    okato = models.ForeignKey(verbose_name='ОКАТО', to='dict.OKATO', blank=True, null=True)
    okpo = models.CharField(verbose_name='ОКПО', max_length=255, blank=True, null=True)
    bank = models.ForeignKey(to='dict.Bank', verbose_name='Банк')
    current_account = models.CharField(verbose_name='Расчетный счет', max_length=255, blank=True, null=True)
    correspondent_account = models.CharField(verbose_name='Корреспондентский счет', max_length=255, blank=True,
                                             null=True)
    #legal_address = AddressWithHouseField(verbose_name='Юридический адрес')
    #actual_address = AddressWithHouseField(verbose_name='Фактический адрес')
    phone = models.CharField(verbose_name='Телефон', max_length=255, blank=True, null=True)
    fax = models.CharField(verbose_name='Факс', max_length=255, blank=True, null=True)
    email = models.EmailField(verbose_name='E-mail', blank=True, null=True)
    website = models.URLField(verbose_name='Web-сайт', blank=True, null=True)
    number_of_employees = models.IntegerField(verbose_name='Общая численность работников', blank=True, null=True)
    has_pension_program = models.BooleanField(verbose_name='Наличие корпоративной пенсионной программы', default=False)
    chief_accountant = models.CharField(verbose_name='ФИО', max_length=255, blank=True, null=True)
    director_fullname = models.CharField(verbose_name='ФИО', max_length=255, blank=True, null=True)
    director_job_title = models.CharField(verbose_name='Должность', max_length=255, blank=True, null=True)
    authority_document_number = models.CharField(verbose_name='Номер', max_length=255, blank=True, null=True)
    authority_document_date = models.DateField(verbose_name='Дата', blank=True, null=True)

    def __str__(self):
        return self.short_name