from npf.core.xmin.admin import XminAdmin


class PersonStateReasonAdmin(XminAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']
    ordering = ['name']
    columns = [{
        'dataIndex': 'name',
        'flex': 1
    }]
