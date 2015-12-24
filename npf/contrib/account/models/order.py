from django.db import models


class Order(models.Model):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.name