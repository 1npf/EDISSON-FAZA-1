from django.db import models


class KeyValueModel(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=512, blank=False, null=False)

    class Meta():
        abstract = True

    def __str__(self):
        return self.code