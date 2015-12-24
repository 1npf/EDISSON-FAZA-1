from django.db import models
from django.contrib.auth.models import User

from npf.contrib.dict.models import DocumentType


class WorkflowProcess(models.Model):
    name = models.CharField(verbose_name='Название', max_length=255, blank=True, null=True)
    document_type = models.ForeignKey(DocumentType, verbose_name='Тип документа',
                                      null=True, blank=True)
    active = models.BooleanField(verbose_name='Активен', default=True)

    class Meta:
        verbose_name = 'Рабочий процесс'
        verbose_name_plural = 'Справочник рабочих процессов'

    def __str__(self):
        return '{} ({})'.format(self.name, self.document_type)


class WorkflowProcessInstance(models.Model):
    process = models.ForeignKey(WorkflowProcess, verbose_name='Рабочий процесс',
                                null=True, blank=True)
    assignment_responsible = models.ForeignKey(User, verbose_name='Ответственный за назначения')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    class Meta:
        verbose_name = 'Рабочий процесс'
        verbose_name_plural = 'Запущенные рабочие процессы'

    def __str__(self):
        return '{} ({})'.format(self.process, self.description)
