from django.db import models

from npf.contrib.subject.models import AbstractSubject, PersonDataMixin
from npf.contrib.common.validators import CyrillicOnlyValidator, BirthdayValidator


class Person(PersonDataMixin, AbstractSubject):

    class Meta:
        verbose_name = 'Физическое лицо'
        verbose_name_plural = 'Вкладчики и участники ФЛ'

    birth_last_name = models.CharField(
        verbose_name='Фамилия при рождении', max_length=255, blank=True, null=True,
        validators=[CyrillicOnlyValidator(message='Фамилия не должна содержать знаки латинского алфавита и цифры',
                                          code='invalid')]
    )

    birth_first_name = models.CharField(
        verbose_name='Имя при рождении', max_length=255, blank=True, null=True,
        validators=[CyrillicOnlyValidator(message='Имя не должно содержать знаки латинского алфавита и цифры',
                                          code='invalid')]
    )


    birth_middle_name = models.CharField(
        verbose_name='Отчество при рождении', max_length=255, blank=True, null=True,
        validators=[CyrillicOnlyValidator(message='Отчество не должно содержать знаки латинского алфавита и цифры',
                                          code='invalid')]
    )

    birth_date = models.DateField(verbose_name='Дата рождения', validators=[BirthdayValidator()])
    birth_place = models.OneToOneField(verbose_name='Место рождения', to='address.Street', related_name='+')

    email = models.EmailField(verbose_name='Адрес электронной почты', blank=True, null=True)
    mobile_phone = models.CharField(verbose_name='Телефон мобильный', max_length=255, blank=True, null=True)
    work_phone = models.CharField(verbose_name='Телефон рабочий', max_length=255, blank=True, null=True)
    home_phone = models.CharField(verbose_name='Телефон домашний', max_length=255, blank=True, null=True)
    passport = models.OneToOneField(verbose_name='Пасспорт', to='subject.PersonPassport', related_name='+',
                                    blank=True, null=True)

    registered_address = models.OneToOneField(verbose_name='Адрес места жительства (регистрации)',
                                                     to='address.House', related_name='+')

    postal_address = models.OneToOneField(verbose_name='Почтовый адрес', to='address.House', null=True,
                                                 blank=True, related_name='+')

    def __str__(self):
        return '{0} {1} {2}'.format(self.last_name, self.first_name, self.middle_name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.name = '{0} {1}.{2}.'.format(self.last_name, self.first_name[:1], self.middle_name[:1])
        super().save(force_insert, force_update, using, update_fields)