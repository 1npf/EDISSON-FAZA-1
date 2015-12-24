from django.db import models

from npf.contrib.dict.models import PensionScheme


class PersonPensionScheme(models.Model):

    class Meta:
        verbose_name = 'Пенсионная схема'
        verbose_name_plural = 'Пенсионные схемы'
        db_table = 'subject_person_pension_scheme'

    person = models.OneToOneField(to='subject.Person', parent_link=True, blank=True, null=True)
    pension_scheme = models.ForeignKey(PensionScheme, verbose_name='Пенсионная схема')

    def __str__(self):
        return self.pension_scheme