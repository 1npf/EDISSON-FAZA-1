from django.db import models

from npf.contrib.subject.models import IdentityDocumentMixin, Person


class PersonBirthCertificate(IdentityDocumentMixin):

    class Meta:
        verbose_name = 'Свидетельство о рождении'
        verbose_name_plural = 'Свидетельства о рождении'
        db_table = 'subject_person_birth_certificate'

    person = models.OneToOneField(Person, parent_link=True, primary_key=True, related_name='birth_certificate')