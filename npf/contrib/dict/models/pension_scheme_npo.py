from django.db import models
from npf.contrib.dict.models import PensionScheme


class PensionSchemeNpo(PensionScheme):
    """
    Справочник пенсионных негосударственного пенсионного обеспечения
    """

    class Meta:
        verbose_name = 'Пенсионная схема НПО'
        verbose_name_plural = 'Пенсионные схемы НПО'
        proxy = True

    class SchemeManager(models.Manager):
        def get_queryset(self):
            return super(PensionSchemeNpo.SchemeManager, self).get_queryset()\
                .filter(type=PensionSchemeNpo.__name__)

    objects = SchemeManager()

