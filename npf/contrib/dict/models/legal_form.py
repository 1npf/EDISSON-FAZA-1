from django.db import models


class LegalForm(models.Model):
    name = models.CharField(verbose_name='Наименование', max_length=255)
    short_name = models.CharField(verbose_name='Краткое наименование', max_length=255)

    class Meta:
        verbose_name = 'Организационно-правовая форма'
        verbose_name_plural = 'Организационно-правовые формы'
        db_table = 'dict_legal_form'

    def __str__(self):
        return '{0} ({1})'.format(self.short_name, self.name)