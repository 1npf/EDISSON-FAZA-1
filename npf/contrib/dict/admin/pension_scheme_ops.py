from npf.core.xmin.admin import XminAdmin

class PensionSchemeOpsAdmin(XminAdmin):
    list_display = ['name']
    list_filter = ['name']
    fields = ['name']
    search_fields = ['name']
    ordering = ['name']
    columns = [{
        'dataIndex': 'name',
        'flex': 1
    }]
