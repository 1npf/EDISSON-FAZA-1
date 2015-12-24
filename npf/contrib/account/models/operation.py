from django.db import models

from npf.contrib.account.models import Order, Account


class Operation(models.Model):
    order = models.ForeignKey(Order)
    bill_credit = models.ForeignKey(Account, related_name='credit_operations')
    bill_debit = models.ForeignKey(Account, related_name='debit_operations')
    sum = models.FloatField()
    status = models.CharField(max_length=255)