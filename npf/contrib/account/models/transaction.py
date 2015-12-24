from django.db import models

from npf.contrib.account.models import Operation


class Transaction(models.Model):
    operation = models.ForeignKey(Operation)
    time = models.DateTimeField(auto_now_add=True)