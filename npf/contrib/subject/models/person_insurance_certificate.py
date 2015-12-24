from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

from npf.core.modelaudit.models import AuditFieldsMixin
from npf.contrib.common.validators import InsuranceCertificateValidator


class PersonInsuranceCertificate(AuditFieldsMixin, models.Model):

    class Meta:
        verbose_name = 'ССГПС'
        verbose_name_plural = 'ССГПС'
        db_table = 'subject_person_insurance_certificate'

    person = models.OneToOneField(to='subject.Person', parent_link=True, blank=True, null=True)

    number = models.CharField(verbose_name='Номер', max_length=11,
                              validators=[MinLengthValidator(11), MaxLengthValidator(11), InsuranceCertificateValidator()])

    original = models.FileField(verbose_name='Оригинал', null=True, blank=True)

    def __str__(self):
        return self.number