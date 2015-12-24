from django.db import models
from npf.contrib.dict.models import PensionScheme


class PensionSchemeOps(PensionScheme):
    """
    Справочник пенсионных схем обязательного пенсионного обеспечения
    """

    class Meta:
        verbose_name = 'Пенсионная схема ОПС'
        verbose_name_plural = 'Пенсионные схемы ОПС'
        proxy = True

    class SchemeManager(models.Manager):
        def get_queryset(self):
            return super(PensionSchemeOps.SchemeManager, self).get_queryset()\
                .filter(type=PensionSchemeOps.__name__)

    objects = SchemeManager()
