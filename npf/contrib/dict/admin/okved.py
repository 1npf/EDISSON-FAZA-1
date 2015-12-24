from mptt.admin import MPTTModelAdmin

from npf.core.xmin.admin import XminAdmin, ExtAdminTreeMixin


class OKVEDAdmin(ExtAdminTreeMixin, XminAdmin, MPTTModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code', 'name']