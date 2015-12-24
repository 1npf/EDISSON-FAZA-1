from django.db import models


class Country(models.Model):

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['short_name']

    name = models.CharField(verbose_name='Наименование', max_length=70)
    short_name = models.CharField(verbose_name='Краткое наименование', max_length=70)

    def __str__(self):
        return '{0} ({1})'.format(self.short_name, self.name)