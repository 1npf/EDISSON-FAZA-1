from django.db import models


class PersonStateReason(models.Model):

    class Meta:
        verbose_name = 'Статус Вкладчика/участника (Основание)'
        verbose_name_plural = 'Основания статуса Вкладчика/участника'
        db_table = 'dict_person_state_reason'

    name = models.CharField(verbose_name='Наименование', max_length=255)

    def __str__(self):
        return self.name