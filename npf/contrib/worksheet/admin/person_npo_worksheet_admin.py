from datetime import datetime

from npf.core.counter.api import Api
from npf.contrib.dict.models import PensionSchemeNpo
from npf.contrib.subject.models import Person, PersonPassport
from npf.contrib.account.models import Account, Contract, ContractPersonNpo
from npf.contrib.worksheet.models import Worksheet
from npf.contrib.worksheet.admin import WorksheetAdmin, WorksheetForm

from npf.core.xmin.admin import XminGenericTabularInline, getter_for_related_field

class PersonWorksheetForm(WorksheetForm):

    # class Meta:
    #     model = Worksheet
    #     fields = '__all__'

    required_fields = [
        'contribution_period', 'person_insurance_certificate', 'person_passport_subdivision_code',
        'person_passport_series', 'person_passport_number', 'person_passport_issued_by', 'person_nationality',
        'pension_scheme', 'end_payment_date', 'start_payment_date', 'person_passport_issue_date', 'person_birth_date',
        'completion_date', 'person_last_name', 'person_first_name', 'person_middle_name', 'person_birth_place__street',
        'person_registered_address__index', 'person_registered_address__street', 'person_registered_address__house']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # tmp = self._meta.fields
        if 'pension_scheme' in self.fields:
            self.fields['pension_scheme'].queryset = PensionSchemeNpo.objects.all()

class PersonNpoWorksheetAdmin(WorksheetAdmin):

    form = PersonWorksheetForm
    model = Worksheet

    list_display = ['completion_date', 'version', 'state', 'number', 'person_last_name', 'person_first_name',
                    'person_middle_name', 'person_sex', 'person_birth_date', 'person_birth_place__street',
                    'person_nationality', 'person_passport_series', 'person_passport_number',
                    'person_passport_issue_date',
                    'person_registered_address__index', 'person_registered_address__street',
                    'person_registered_address__house', 'person_registered_address__corps',
                    'person_registered_address__apartment',
                    'start_payment_date',
                    'end_payment_date', 'contribution_period', 'regular_payment', 'pension_scheme',
                    'transfer_rights_date', 'added_at', 'added_by_user']

    list_filter = ['completion_date', 'version', 'number', 'person_last_name',
                   'person_first_name', 'person_middle_name', 'person_sex', 'person_birth_date',
                   'person_birth_place__street', 'person_nationality', 'person_passport_series',
                   'person_passport_number', 'person_passport_issue_date',
                   'person_registered_address__index', 'person_registered_address__street',
                   'person_registered_address__house', 'person_registered_address__corps',
                   'person_registered_address__apartment',
                   'start_payment_date',
                   'end_payment_date', 'contribution_period', 'regular_payment', 'pension_scheme',
                   'transfer_rights_date', 'added_at', 'added_by_user']

    # Место рождения

    person_birth_place__street = getter_for_related_field('person_birth_place__street',
                                                          short_description='Место рождения')

    # Адрес места жительства (регистрации) Вкладчика

    person_registered_address__index = getter_for_related_field('person_registered_address__index',
                                                                short_description='Почтовый индекс')

    person_registered_address__street = getter_for_related_field('person_registered_address__street',
                                                                 short_description='Улица')

    person_registered_address__house = getter_for_related_field('person_registered_address__house',
                                                                short_description='Дом')

    person_registered_address__corps = getter_for_related_field('person_registered_address__corps',
                                                                short_description='Корпус')

    person_registered_address__apartment = getter_for_related_field('person_registered_address__apartment',
                                                                    short_description='Квартира')
    # Почтовый адрес Вкладчика

    person_postal_address__index = getter_for_related_field('person_postal_address__index',
                                                            short_description='Почтовый индекс')

    person_postal_address__street = getter_for_related_field('person_postal_address__street',
                                                             short_description='Улица')

    person_postal_address__house = getter_for_related_field('person_postal_address__house',
                                                            short_description='Дом')

    person_postal_address__corps = getter_for_related_field('person_postal_address__corps',
                                                            short_description='Корпус')

    person_postal_address__apartment = getter_for_related_field('person_postal_address__apartment',
                                                                short_description='Квартира')

    columns = [{
        'dataIndex': 'completion_date',
        'width': 200,
    }, {
        'dataIndex': 'number',
        'width': 150,
    }, {
        'text': 'Статус',
        'dataIndex': 'state'
    }, {
        'text': 'Регулярные взносы',
        'columns': [{
            'dataIndex': 'start_payment_date'
        }, {
            'dataIndex': 'end_payment_date'
        }, {
            'text': 'Переодичность',
            'dataIndex': 'contribution_period',
            'width': 140
        }, {
            'dataIndex': 'regular_payment',
            'width': 210
        }, {
            'dataIndex': 'pension_scheme',
            'width': 160
        }, {
            'dataIndex': 'transfer_rights_date',
            'width': 170
        }]
    }, {
        'text': 'Вкладчик',
        'columns': [{
            'dataIndex': 'person_last_name',
            'width': 105
        }, {
            'dataIndex': 'person_first_name',
            'width': 105
        }, {
            'dataIndex': 'person_middle_name',
            'width': 110
        }, {
            'dataIndex': 'person_sex'
        }, {
            'dataIndex': 'person_birth_date',
            'width': 140
        }, {
            'dataIndex': 'person_birth_place__street',
            'width': 200,
            'filter': 'address'
        }, {
            'dataIndex': 'person_nationality',
            'width': 200
        }, {
            'text': 'Адрес места жительства (регистрации)',
            'columns': [{
                'dataIndex': 'person_registered_address__index',
                'width': 110,
                'filter': 'string'
            }, {
                'dataIndex': 'person_registered_address__street',
                'width': 350,
                'filter': 'address'
            }, {
                'dataIndex': 'person_registered_address__house',
                'filter': 'string'
            }, {
                'dataIndex': 'person_registered_address__corps',
                'filter': 'string'
            }, {
                'dataIndex': 'person_registered_address__apartment',
                'filter': 'string'
            }]
        }, {
            'text': 'Паспорт',
            'columns': [{
                'dataIndex': 'person_passport_series'
            }, {
                'dataIndex': 'person_passport_number'
            }, {
                'dataIndex': 'person_passport_issue_date',
                'width': 130
            }]
        }]
    }, {
        'text': 'Служебная информация',
        'columns': [{
            'dataIndex': 'added_at',
            'width': 190
        }, {
            'text': 'Кем создано',
            'dataIndex': 'added_by_user',
            'width': 150
        }]
    }]

    fieldsets = (
        (None, {'fields': ['completion_date']}),
        ('Участник', {'fields': [
            'person_last_name', 'person_first_name', 'person_middle_name', 'person_birth_date', 'person_nationality',
            'person_birth_place__street']}),
        ('Адрес регистрации', {'fields': [
            'person_registered_address__index', 'person_registered_address__street', 'person_registered_address__house',
            'person_registered_address__corps', 'person_registered_address__apartment']}),
        ('Адрес почты', {'fields': [
            'person_postal_address_same_as_registered_address', 'person_postal_address__index',
            'person_postal_address__street', 'person_postal_address__house', 'person_postal_address__corps',
            'person_postal_address__apartment']}),
        ('Контакты', {'fields': ['person_phone', 'person_email']}),
        ('Паспорт', {'fields': [
            'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
            'person_passport_subdivision_code', 'person_passport_issued_by']}),
        ('Страховое свидетельство гос. пенсионного страхования', {'fields': ['person_insurance_certificate']}),
        ('Регулярные взносы (не менее 5 лет)', {'fields': [
            'pension_scheme', 'contribution_period', 'start_payment_date', 'end_payment_date', 'regular_payment']}),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return super().get_fieldsets(request, obj)
        return (
            (None, {'fields': ['number', 'completion_date']}),
            ('Вкладчик', {'fields': ['person_last_name', 'person_first_name', 'person_middle_name', 'person_sex',
                                     'person_birth_date', 'person_nationality', 'person_birth_place']}),
            ('Контакты', {'fields': ['person_registered_address', 'person_postal_address', 'person_phone',
                                     'person_email']}),
            ('Паспорт', {'fields': ['person_passport_series', 'person_passport_number', 'person_passport_issue_date',
                                    'person_passport_subdivision_code', 'person_passport_issued_by']}),
            ('Страховое свидетельство гос. пенсионного страхования', {'fields': ['person_insurance_certificate']}),
            ('Регулярные взносы (не менее 5 лет)', {'fields': ['pension_scheme', 'contribution_period',
                                                               'start_payment_date', 'end_payment_date',
                                                               'regular_payment']}),
        )

    def commit_final_version_worksheet(self, request, obj: Worksheet):
        """
        Подтверждение финальной версии анкеты и создание договора
        """
        if obj.number:
            return

        year = datetime.now().strftime('%y')

        # Присвоение номера договора
        obj.number = Api('0000-{counter_fl_' + year + '}/' + year).generate()
        obj.save(update_fields=['number'])

        person = Person.objects.filter(
            last_name=obj.person_last_name,
            first_name=obj.person_first_name,
            middle_name=obj.person_middle_name,
            birth_date=obj.person_birth_date,
            birth_place=obj.person_birth_place,
            sex=obj.person_sex,
            nationality=obj.person_nationality,
            passport__series=obj.person_passport_series,
            passport__number=obj.person_passport_number,
            passport__issue_date=obj.person_passport_issue_date)[:1]

        if not person:
            person = Person.objects.create(
                last_name=obj.person_last_name,
                first_name=obj.person_first_name,
                middle_name=obj.person_middle_name,
                birth_date=obj.person_birth_date,
                birth_place=obj.person_birth_place,
                sex=obj.person_sex,
                email=obj.person_email,
                mobile_phone=obj.person_phone,
                nationality=obj.person_nationality,
                registered_address=obj.person_registered_address,
                postal_address=obj.person_postal_address,
                added_by_user=request.user,
                modified_by_user=request.user
            )

            person.passport = PersonPassport.objects.create(
                series=obj.person_passport_series,
                number=obj.person_passport_number,
                issue_date=obj.person_passport_issue_date,
                issued_by=obj.person_passport_issued_by,
                subdivision_code=obj.person_passport_subdivision_code,
                added_by_user=request.user,
                modified_by_user=request.user,
                person=person
            )

        else:
            person = person[0]

        account = Account.objects.create(
            number=obj.number,
            investor=person,
            participant=person,
            opened_at=obj.added_at,
            state=Account.State.OPEN,
            type=Account.Type.CUMULATIVE,
            added_by_user=request.user,
            modified_by_user=request.user,
        )

        ContractPersonNpo.objects.create(
            account=account,
            state=Contract.State.CONCLUDED,
            conclusion_date=obj.added_at.date(),
            pension_scheme=obj.pension_scheme,
            contribution_period=obj.contribution_period,
            regular_payment_percent=obj.regular_payment,
            start_payment_date=obj.start_payment_date,
            end_payment_date=obj.end_payment_date,
            added_by_user=request.user,
            modified_by_user=request.user,
        )