from django.db import models


class NamedCounter(models.Model):

    class Meta:
        verbose_name = 'Счетчик'
        verbose_name_plural = 'Системные счетчики'
        db_table = 'counter_named_counter'

    name = models.CharField(max_length=255, unique=True)
    value = models.PositiveIntegerField(default=1)