from django.db import models

from npf.contrib.worksheet.models import Worksheet


class CorrectionData(models.Model):

    class Meta:
        verbose_name = 'Коррекция данных (двойной ввод)'
        verbose_name_plural = 'Коррекция данных (двойной ввод)'
        db_table = 'worksheet_correction_data'
        ordering = ['label']

    xtype = models.CharField(max_length=255)
    field = models.CharField(max_length=255)
    label = models.CharField(verbose_name='Поле', max_length=255)
    first_value = models.CharField(verbose_name='Первый ввод', max_length=255, blank=True, null=True)
    first_value_display = models.CharField(max_length=255, blank=True, null=True)
    second_value = models.CharField(verbose_name='Второй ввод', max_length=255, blank=True, null=True)
    second_value_display = models.CharField(max_length=255, blank=True, null=True)
    worksheet = models.ForeignKey(verbose_name='Анкета', to=Worksheet)