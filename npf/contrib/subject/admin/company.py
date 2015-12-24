from npf.core.modelaudit.admin import AuditFieldsAdminMixin
from npf.core.xmin.admin import XminAdmin


class CompanyAdmin(AuditFieldsAdminMixin, XminAdmin):
    fieldsets = (
        (None, {'fields': ['legal_form', 'short_name', 'full_name', 'second_name', 'ogrn', 'inn', 'kpp',
                           'number_of_employees', 'has_pension_program']}),
        ('Руководитель', {'fields': ['director_fullname', 'director_job_title']}),
        ('Документ подтверждающий полномочия руководителя', {'fields': ['authority_document_number',
                                                                        'authority_document_date']}),
        ('Главный бухгалтер', {'fields': ['chief_accountant']}),
        ('Контакты', {'fields': ['legal_address', 'actual_address', 'phone', 'fax', 'email', 'website']}),
        ('Код отрасли', {'fields': ['okved', 'okato', 'okpo']}),
        ('Запись в едином государственном реестре', {'fields': ['register_number', 'register_date', 'register_entry']}),
        ('Банковские реквизиты', {'fields': ['bank', 'current_account', 'correspondent_account']}),
    )

    class Media:
        js = ['//ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.js']