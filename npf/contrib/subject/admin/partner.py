from npf.core.xmin.admin import XminAdmin


class PartnerAdmin(XminAdmin):
    list_display = ['name']
    fields = ['name']
    readonly_fields = ['name']
    ordering = ['name']

    def has_add_permission(self, request):
        return False