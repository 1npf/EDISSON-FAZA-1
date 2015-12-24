from django.contrib import admin

# from .person import PersonAdmin
# from .company import CompanyAdmin
# from .partner import PartnerAdmin
from .pension_fund_admin import PensionFundAdmin

from npf.contrib.subject import models as subject


# admin.site.register(subject.Person, PersonAdmin)
admin.site.register(subject.PensionFund, PensionFundAdmin)
