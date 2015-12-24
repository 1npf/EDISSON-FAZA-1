from mptt.admin import MPTTModelAdmin

from npf.core.xmin.admin import XminAdmin, ExtAdminTreeMixin


class BankAdmin(ExtAdminTreeMixin, XminAdmin, MPTTModelAdmin):
    list_display = ['name', 'bik']
    search_fields = ['name', 'bik']
    ordering = ['name']
