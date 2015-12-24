from django.db import models

from npf.contrib.subject.models import IdentityDocumentMixin


class PersonPassport(IdentityDocumentMixin):

    class Meta:
        verbose_name = 'Пасспорт'
        verbose_name_plural = 'Списпок паспортов'
        db_table = 'subject_person_passport'

    person = models.ForeignKey(to='subject.Person', related_name='passports', blank=True, null=True)
    subdivision_code = models.CharField(verbose_name='Код подразделения', max_length=7)