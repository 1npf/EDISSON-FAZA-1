from mptt.admin import MPTTModelAdmin

from npf.core.xmin.admin import XminAdmin, ExtAdminTreeMixin


class OKATOAdmin(ExtAdminTreeMixin, XminAdmin, MPTTModelAdmin):
    list_display = ['name', 'additional_info', 'code']
    search_fields = ['name', 'additional_info', 'code']