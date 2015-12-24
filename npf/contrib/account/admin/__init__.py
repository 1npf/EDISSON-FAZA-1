from django.contrib import admin

from npf.core.xmin.admin import XminAdmin
from npf.contrib.account.models import Account, ContractPersonNpo
from .contract_person_npo import ContractPersonNpoAdmin


admin.site.register(Account, XminAdmin)
admin.site.register(ContractPersonNpo, ContractPersonNpoAdmin)

