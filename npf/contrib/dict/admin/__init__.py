from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from npf.contrib.dict import models as dict
# from .bank import BankAdmin
from .legal_form import LegalFormAdmin
# from .country import CountryAdmin
from .document_type import DocumentTypeAdmin
# from .okved import OKVEDAdmin
# from .okato import OKATOAdmin
# from .pension_scheme_ops import PensionSchemeOpsAdmin
# from .pension_scheme_npo import PensionSchemeNpoAdmin
# from .person_state_reason import PersonStateReasonAdmin


# admin.site.register(dict.PersonStateReason, PersonStateReasonAdmin)
admin.site.register(dict.LegalForm, LegalFormAdmin)
# admin.site.register(dict.Bank, BankAdmin)
# admin.site.register(dict.Country, CountryAdmin)
# admin.site.register(dict.OKVED, OKVEDAdmin)
# admin.site.register(dict.OKATO, OKATOAdmin)
# admin.site.register(dict.PensionSchemeOps, PensionSchemeOpsAdmin)
# admin.site.register(dict.PensionSchemeNpo, PensionSchemeNpoAdmin)
admin.site.register(dict.DocumentType, DocumentTypeAdmin)
