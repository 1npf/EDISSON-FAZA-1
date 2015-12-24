from django.db import models


class PensionScheme(models.Model):
    """
    Справочник пенсионных схем
    """

    class Meta:
        verbose_name = 'Пенсионная схема'
        verbose_name_plural = 'Пенсионные схемы'
        db_table = 'dict_pension_scheme'

    name = models.CharField(verbose_name='Наименование', max_length=255)
    type = models.CharField(verbose_name='Тип', max_length=255, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.type = self.__class__.__name__
        super().save(*args, **kwargs)
