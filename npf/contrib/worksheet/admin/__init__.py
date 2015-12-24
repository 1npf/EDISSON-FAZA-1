from django.contrib import admin

from .worksheet_admin import WorksheetAdmin, WorksheetForm, WorksheetStateFilter, CorrectionDataForm, CorrectionDataInline
from .person_npo_worksheet_admin import PersonNpoWorksheetAdmin
from .person_ops_worksheet_admin import PersonOpsWorksheetAdmin
from .third_person_npo_worksheet_admin import ThirdPersonNpoWorksheetAdmin

from npf.contrib.worksheet.models import *


admin.site.register(PersonOpsWorksheet, PersonOpsWorksheetAdmin)
admin.site.register(PersonNpoWorksheet, PersonNpoWorksheetAdmin)
admin.site.register(ThirdPersonNpoWorksheet, ThirdPersonNpoWorksheetAdmin)
