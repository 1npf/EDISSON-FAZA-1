from django.db import models

from npf.contrib.common.validators import CyrillicOnlyValidator


class PersonDataMixin(models.Model):

    class Meta:
        abstract = True

    class Sex:
        MALE = 'm'
        FEMALE = 'f'
        CHOICES = (
            (MALE, 'Мужской'),
            (FEMALE, 'Женский'),
        )

    last_name = models.CharField(
        verbose_name='Фамилия', max_length=255,
        validators=[CyrillicOnlyValidator(message='Фамилия не должна содержать знаки латинского алфавита и цифры',
                                          code='invalid')]
    )

    first_name = models.CharField(
        verbose_name='Имя', max_length=255,
        validators=[CyrillicOnlyValidator(message='Имя не должно содержать знаки латинского алфавита и цифры',
                                          code='invalid')]
    )

    middle_name = models.CharField(
        verbose_name='Отчество', max_length=255,
        validators=[CyrillicOnlyValidator(message='Отчество не должно содержать знаки латинского алфавита и цифры',
                                          code='invalid')]
    )

    sex = models.CharField(verbose_name='Пол', max_length=1, choices=Sex.CHOICES)
    nationality = models.ForeignKey(verbose_name='Гражданство', to='dict.Country')
    #registered_address = AddressWithHouseField(verbose_name='Адрес места жительства (регистрации)')
    #postal_address = AddressWithHouseField(verbose_name='Почтовый адрес')