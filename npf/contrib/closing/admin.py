from django.contrib import admin

from npf.core.modelaudit.admin import AuditFieldsAdminMixin
from npf.contrib.closing.models import *
from npf.core.xmin.admin import XminAdmin


class StatementAdmin(AuditFieldsAdminMixin, XminAdmin):
    pass


admin.site.register(Statement, StatementAdmin)