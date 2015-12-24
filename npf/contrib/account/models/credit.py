from django.db import models

from npf.contrib.account.models import KeyValueModel, Order


class Credit(KeyValueModel):
    credit = models.ForeignKey(Order)