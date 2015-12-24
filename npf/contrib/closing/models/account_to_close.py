from django.db import models

from npf.contrib.account.models import Account
from npf.core.workflow.models import WorkflowProcess


class AccountToClose(models.Model):
    account = models.ForeignKey(Account)
    process = models.ForeignKey(WorkflowProcess)