from django.db import models

from npf.contrib.account.models import KeyValueModel, Order


class Debit(KeyValueModel):
    debit = models.ForeignKey(Order)