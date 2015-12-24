from django.db import models
from django.contrib.contenttypes.models import ContentType


class Template(models.Model):

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны печатных форм'

    name = models.CharField(verbose_name='Название', max_length=150)
    file_name = models.CharField(verbose_name='Название генерируемого файла', max_length=250)
    file = models.FileField(verbose_name="Шаблон")
    model = models.ForeignKey(ContentType, null=True, verbose_name="Модель")
    instructions = models.CharField(verbose_name='Инструкции к шаблону', max_length=450)

    def __str__(self):
        return self.name