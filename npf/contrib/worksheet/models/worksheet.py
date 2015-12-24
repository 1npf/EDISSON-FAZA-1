from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.encoding import force_text
from django.utils.functional import cached_property
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator

from npf.core.modelaudit.models import AuditFieldsMixin
from npf.contrib.common.validators import (CyrillicOnlyValidator, DigitOnlyValidator, MiddleNameValidator,
                                           InsuranceCertificateValidator, BirthdayValidator)

from npf.contrib.subject.models import Person
from npf.contrib.account.models import Contract


class IdentityDocumentType:
    PASSPORT = 'p'
    BIRTH_CERTIFICATE = 'b'
    CHOICES = (
        (PASSPORT, 'Паспорт'),
        (BIRTH_CERTIFICATE, 'Свидетельство о рождении'),
    )


class Worksheet(AuditFieldsMixin, models.Model):

    class Meta:
        verbose_name = 'Анкета Вкладчика/участника ФЛ'
        verbose_name_plural = 'Реестр анкет вкладчиков и участников ФЛ'
        db_table = 'worksheet_worksheet'

    class State:
        WAIT_SECOND_INPUT = 'wsi'
        WAIT_CORRECTION = 'wc'
        COMMIT = 'c'
        CHOICES = (
            (WAIT_SECOND_INPUT, 'Ожидание второго ввода'),
            (WAIT_CORRECTION, 'Ожидание коррекции данных'),
            (COMMIT, 'Первый и второй ввод осуществлен'),
        )

    type = models.CharField(verbose_name='Тип', max_length=255, db_index=True)
    number = models.CharField(verbose_name='Номер договора', max_length=255, null=True, blank=True, db_index=True)

    completion_date = models.DateField(
        verbose_name='Дата заполнения анкеты',
        help_text='Укажите дату заполнения клиентом, бумажного экземпляра анкеты',
        db_index=True
    )

    file = models.FileField(verbose_name='Скан', null=True, blank=True)
    version = models.PositiveSmallIntegerField(verbose_name='Версия', default=0, db_index=True)
    current_version = models.PositiveSmallIntegerField(verbose_name='Текущая версия', default=0, db_index=True)

    content_type = models.ForeignKey(ContentType, null=True, blank=True, db_index=True)
    object_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # Вкладчик
    person_last_name = models.CharField(
        verbose_name='Фамилия', max_length=255, blank=True, null=True,
        help_text='Обязательное поле. Только буквы кирилицы.',
        validators=[
            CyrillicOnlyValidator(message='Фамилия не должна содержать знаки латинского алфавита и цифры',
                                  code='invalid')
        ]
    )

    person_first_name = models.CharField(
        verbose_name='Имя', max_length=255, blank=True, null=True,
        help_text='Обязательное поле. Только буквы кирилицы.',
        validators=[
            CyrillicOnlyValidator(message='Имя не должно содержать знаки латинского алфавита и цифры', code='invalid')
        ]
    )

    person_middle_name = models.CharField(
        verbose_name='Отчество', max_length=255, blank=True, null=True,
        help_text='Обязательное поле. Только буквы кирилицы. Окончание на -вич или -вна.',
        validators=[
            CyrillicOnlyValidator(message='Отчество не должно содержать знаки латинского алфавита и цифры',
                                  code='invalid'),
            MiddleNameValidator()
        ]
    )

    person_birth_last_name = models.CharField(
        verbose_name='Фамилия при рождении', max_length=255, blank=True, null=True,
        help_text='Обязательное поле. Только буквы кирилицы.',
        validators=[CyrillicOnlyValidator(message='Фамилия не должна содержать знаки латинского алфавита и цифры',
                                          code='invalid')]
    )

    person_birth_first_name = models.CharField(
        verbose_name='Имя при рождении', max_length=255, blank=True, null=True,
        help_text='Обязательное поле. Только буквы кирилицы.',
        validators=[CyrillicOnlyValidator(message='Имя не должно содержать знаки латинского алфавита и цифры',
                                          code='invalid')]
    )

    person_birth_middle_name = models.CharField(
        verbose_name='Отчество при рождении', max_length=255, blank=True, null=True,
        help_text='Обязательное поле. Только буквы кирилицы. Окончание на -вич или -вна.',
        validators=[CyrillicOnlyValidator(message='Отчество не должно содержать знаки латинского алфавита и цифры',
                                          code='invalid')]
    )

    person_birth_date = models.DateField(verbose_name='Дата рождения', validators=[BirthdayValidator()])
    person_birth_place = models.OneToOneField(verbose_name='Место рождения', to='address.Street', related_name='+')

    person_sex = models.CharField(verbose_name='Пол', max_length=1, choices=Person.Sex.CHOICES)
    person_nationality = models.ForeignKey(verbose_name='Гражданство', to='dict.Country', related_name='+')

    person_registered_address = models.OneToOneField(verbose_name='Адрес места жительства (регистрации)',
                                                     to='address.House', related_name='+')

    person_postal_address = models.OneToOneField(verbose_name='Почтовый адрес', to='address.House', null=True,
                                                 blank=True, related_name='+')

    person_phone = models.CharField(verbose_name='Телефон мобильный', max_length=255, blank=True, null=True)
    person_email = models.EmailField(verbose_name='Адрес электронной почты', blank=True, null=True)

    person_passport_series = models.CharField(verbose_name='Серия', max_length=4,
                                              validators=[MinLengthValidator(4), MaxLengthValidator(4),
                                                          DigitOnlyValidator()])

    person_passport_number = models.CharField(verbose_name='Номер', max_length=6,
                                              validators=[MinLengthValidator(6), MaxLengthValidator(6),
                                                          DigitOnlyValidator()])

    person_passport_issue_date = models.DateField(verbose_name='Дата выдачи')
    person_passport_subdivision_code = models.CharField(verbose_name='Код подразделения', max_length=7)
    person_passport_issued_by = models.CharField(verbose_name='Кем выдан', max_length=255)
    person_passport_file = models.FileField(verbose_name='Скан', null=True, blank=True)

    person_insurance_certificate = models.CharField(
        verbose_name='Номер', max_length=11, blank=True, null=True,
        validators=[MinLengthValidator(11), MaxLengthValidator(11)]
    )

    person_insurance_certificate_file = models.FileField(verbose_name='Скан', null=True, blank=True)

    # Участник (3-е лицо)
    third_person_last_name = models.CharField(
        verbose_name='Фамилия', max_length=255, blank=True, null=True,
        help_text='Обязательное поле. Только буквы кирилицы.',
        validators=[
            CyrillicOnlyValidator(message='Фамилия не должна содержать знаки латинского алфавита и цифры',
                                  code='invalid')
        ]
    )

    third_person_first_name = models.CharField(
        verbose_name='Имя', max_length=255, blank=True, null=True,
        help_text='Обязательное поле. Только буквы кирилицы.',
        validators=[
            CyrillicOnlyValidator(message='Имя не должно содержать знаки латинского алфавита и цифры', code='invalid')
        ]
    )

    third_person_middle_name = models.CharField(
        verbose_name='Отчество', max_length=255, blank=True, null=True,
        help_text='Обязательное поле. Только буквы кирилицы. Окончание на -вич или -вна.',
        validators=[
            CyrillicOnlyValidator(message='Отчество не должно содержать знаки латинского алфавита и цифры',
                                  code='invalid'),
            MiddleNameValidator()
        ]
    )

    third_person_birth_date = models.DateField(verbose_name='Дата рождения', blank=True, null=True,
                                               validators=[BirthdayValidator()])

    third_person_birth_place = models.OneToOneField(verbose_name='Место рождения', to='address.Street',
                                                    related_name='+', blank=True, null=True,)

    third_person_sex = models.CharField(verbose_name='Пол', max_length=1, choices=Person.Sex.CHOICES, blank=True,
                                        null=True)

    third_person_nationality = models.ForeignKey(verbose_name='Гражданство', to='dict.Country', related_name='+',
                                                 blank=True, null=True)

    third_person_registered_address = models.OneToOneField(verbose_name='Адрес места жительства (регистрации)',
                                                           to='address.House', related_name='+', blank=True, null=True)

    third_person_postal_address = models.OneToOneField(verbose_name='Почтовый адрес', to='address.House', null=True,
                                                       blank=True, related_name='+')

    third_person_phone = models.CharField(verbose_name='Телефон мобильный', max_length=255, blank=True, null=True)
    third_person_email = models.EmailField(verbose_name='Адрес электронной почты', blank=True, null=True)

    third_person_document_type = models.CharField(verbose_name='Тип документа', max_length=1,
                                                  choices=IdentityDocumentType.CHOICES,
                                                  default=IdentityDocumentType.PASSPORT,
                                                  blank=True, null=True)

    third_person_document_series = models.CharField(verbose_name='Серия', max_length=255, blank=True, null=True)
    third_person_document_number = models.CharField(verbose_name='Номер', max_length=255, blank=True, null=True)
    third_person_document_issue_date = models.DateField(verbose_name='Дата выдачи', blank=True, null=True)

    third_person_document_subdivision_code = models.CharField(verbose_name='Код подразделения',
                                                              help_text='Обязательно при заполнении паспорта',
                                                              max_length=7, blank=True, null=True)

    third_person_document_issued_by = models.CharField(verbose_name='Кем выдан', max_length=255, blank=True, null=True)
    third_person_document_file = models.FileField(verbose_name='Скан', null=True, blank=True)

    third_person_insurance_certificate = models.CharField(
        verbose_name='Номер', max_length=11, blank=True, null=True,
        validators=[MinLengthValidator(11), MaxLengthValidator(11), InsuranceCertificateValidator()]
    )

    third_person_insurance_certificate_file = models.FileField(verbose_name='Скан', null=True, blank=True)

    # Данные договора
    pension_scheme = models.ForeignKey(verbose_name='Пенсионная схема', to='dict.PensionScheme')

    contribution_period = models.CharField(verbose_name='Переодичность взносов',
                                           max_length=1,
                                           choices=Contract.ContributionPeriod.CHOICES,
                                           default=Contract.ContributionPeriod.MONTH,
                                           db_index=True)

    regular_payment = models.PositiveIntegerField(verbose_name='Размер взноса (% МРОТ)', default=10,
                                                  validators=[MinValueValidator(10)])

    start_payment_date = models.DateField(verbose_name='С')
    end_payment_date = models.DateField(verbose_name='По')

    transfer_rights_date = models.DateField(
        verbose_name='Дата перехода прав',
        help_text='Дата перехода прав Участнику на средства, учтенные на пенсионном счете, открытом на его имя.',
        blank=True,
        null=True
    )

    previous_insurer = models.ForeignKey(verbose_name='Предыдущий страховщик', to='subject.PensionFund',
                                         related_name='+', blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.type = self.__class__.__name__

        if self.person_middle_name[-3:] == 'вич':
            self.person_sex = Person.Sex.MALE
        elif self.person_middle_name[-3:] == 'вна':
            self.person_sex = Person.Sex.FEMALE

        if self.third_person_middle_name and self.third_person_middle_name[-3:] == 'вич':
            self.third_person_sex = Person.Sex.MALE
        elif self.third_person_middle_name and self.third_person_middle_name[-3:] == 'вна':
            self.third_person_sex = Person.Sex.FEMALE

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return '{0} {1}. {2}. от {3}'.format(self.person_last_name, self.person_first_name[:1],
                                             self.person_middle_name[:1], self.completion_date.strftime('%d.%m.%Y'))

    @cached_property
    def state(self):
        if self.version == 0:
            return Worksheet.State.WAIT_SECOND_INPUT
        if self.version in [1, 2] and not self.number:
            return Worksheet.State.WAIT_CORRECTION
        if self.number:
            return Worksheet.State.COMMIT

    @cached_property
    def state_display(self):
        return force_text(dict(Worksheet.State.CHOICES).get(self.state, self.state), strings_only=True)
