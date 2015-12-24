from django.db import models

from npf.core.modelaudit.models import AuditFieldsMixin
from npf.contrib.subject.models import PersonDataMixin


class PersonDataHistory(AuditFieldsMixin, PersonDataMixin, models.Model):

    class Meta:
        verbose_name = 'История персональных данных'
        verbose_name_plural = 'История персональных данных'
        db_table = 'subject_person_data_history'

    person = models.ForeignKey(to='subject.Person', verbose_name='Физическое лицо', related_name='history')
    date = models.DateField(verbose_name='Дата')
    passport = models.ForeignKey(to='subject.PersonPassport', verbose_name='Пасспорт', null=True)

    def __str__(self):
        return str(self.person)