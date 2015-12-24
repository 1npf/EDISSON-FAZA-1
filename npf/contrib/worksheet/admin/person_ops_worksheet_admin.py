from datetime import datetime

from django import forms

from npf.contrib.account.models import Account, ContractPersonNpo, Contract
from npf.contrib.subject.models import Person, PersonPassport
from npf.contrib.dict.models import PensionSchemeOps
from npf.core.counter.api import Api
from npf.contrib.worksheet.models import Worksheet
from npf.contrib.worksheet.admin import WorksheetAdmin, WorksheetForm, WorksheetStateFilter

from npf.core.xmin.admin import XminGenericTabularInline, getter_for_related_field



class PersonOpsWorksheetForm(WorksheetForm):

    required_fields = [
        'completion_date', 'contribution_period', 'regular_payment', 'previous_insurer', 'pension_scheme',
        'end_payment_date', 'start_payment_date', 'person_passport_issue_date', 'person_birth_date',
        'person_insurance_certificate', 'person_passport_subdivision_code', 'person_passport_series',
        'person_passport_number', 'person_passport_issued_by', 'person_nationality', 'person_birth_place__street',
        'person_registered_address__index', 'person_registered_address__street', 'person_registered_address__house',
        'person_birth_last_name', 'person_birth_first_name', 'person_birth_middle_name', 'person_insurance_certificate']

    person_last_name_not_changed = forms.BooleanField(
        label='Не менялось с рождения',
        help_text='Отметьте, если Фамилия застрахованного лица не менялась с рождения. '
                  'Будет использоваться значение указанное в поле "Фамилия при рождении".',
        initial=True)

    person_first_name_not_changed = forms.BooleanField(
        label='Не менялось с рождения',
        help_text='Отметьте, если Имя застрахованного лица не мелось с рождения. '
                  'Будет использоваться значение указанное в поле "Имя при рождении".',
        initial=True)

    person_middle_name_not_changed = forms.BooleanField(
        label='Не менялось с рождения',
        help_text='Отметьте, если Отчество застрахованного лица не менялось с рождения. '
                  'Будет использоваться значение указанное в поле "Отчество при рождении".',
        initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.fields['pension_scheme'].queryset = PensionSchemeOps.objects.all()
        except KeyError:
            pass

        try:
            person_last_name_required = not (True if not self.data
                                             else self.data.get('person_last_name_not_changed') == 'on')

            self.fields['person_last_name'].help_text = 'Обязательное поле, если Фамилия ЗЛ изменялась с момента ' \
                                                        'рождения.'

            self.fields['person_last_name'].required = person_last_name_required
        except KeyError:
            pass

        try:
            person_first_name_required = not (True if not self.data
                                              else self.data.get('person_first_name_not_changed') == 'on')

            self.fields['person_first_name'].help_text = 'Обязательное поле, если Имя ЗЛ изменялось с момента рождения.'

            self.fields['person_first_name'].required = person_first_name_required
        except KeyError:
            pass

        try:
            person_middle_name_required = not (True if not self.data
                                               else self.data.get('person_middle_name_not_changed') == 'on')

            self.fields['person_middle_name'].help_text = 'Обязательное поле, если Отчетво ЗЛ изменялось с момента ' \
                                                          'рождения.'

            self.fields['person_middle_name'].required = person_middle_name_required
        except KeyError:
            pass

    def save(self, commit=True):
        instance = super().save(commit)

        person_last_name_not_changed = self.cleaned_data.get('person_last_name_not_changed')
        person_first_name_not_changed = self.cleaned_data.get('person_first_name_not_changed')
        person_middle_name_not_changed = self.cleaned_data.get('person_middle_name_not_changed')

        person_last_name = self.cleaned_data.get('person_last_name')
        person_first_name = self.cleaned_data.get('person_first_name')
        person_middle_name = self.cleaned_data.get('person_middle_name')

        person_birth_last_name = self.cleaned_data.get('person_birth_last_name')
        person_birth_first_name = self.cleaned_data.get('person_birth_first_name')
        person_birth_middle_name = self.cleaned_data.get('person_birth_middle_name')

        if person_last_name_not_changed and not person_last_name and person_birth_last_name:
            instance.person_last_name = person_birth_last_name

        if person_first_name_not_changed and not person_first_name and person_birth_first_name:
            instance.person_first_name = person_birth_first_name

        if person_middle_name_not_changed and not person_middle_name and person_birth_middle_name:
            instance.person_middle_name = person_birth_middle_name

        return instance


class WorksheetInputHistoryInline(XminGenericTabularInline):
    verbose_name_plural = 'История двойного ввода'
    model = Worksheet
    extra = 0

    fields = [
        'completion_date', 'version', 'number', 'previous_insurer', 'person_last_name', 'person_first_name',
        'person_middle_name', 'person_birth_last_name', 'person_birth_first_name', 'person_birth_middle_name',
        'person_sex', 'person_birth_date', 'person_birth_place__street',
        'person_nationality', 'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
        'person_registered_address__index', 'person_registered_address__street', 'person_registered_address__house',
        'person_registered_address__corps', 'person_registered_address__apartment', 'person_insurance_certificate',
        'start_payment_date', 'end_payment_date', 'contribution_period', 'regular_payment', 'pension_scheme',
        'added_at', 'added_by_user']

    list_filter = [
        'completion_date', 'version', 'number', 'previous_insurer', WorksheetStateFilter, 'person_last_name',
        'person_first_name', 'person_middle_name', 'person_birth_last_name', 'person_birth_first_name',
        'person_birth_middle_name', 'person_sex', 'person_birth_date', 'person_birth_place__street',
        'person_nationality', 'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
        'person_registered_address__index', 'person_registered_address__street', 'person_registered_address__house',
        'person_registered_address__corps', 'person_registered_address__apartment', 'person_insurance_certificate',
        'start_payment_date', 'end_payment_date', 'contribution_period', 'regular_payment', 'pension_scheme',
        'added_at', 'added_by_user']

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
        'text': 'Служебная информация',
        'columns': [{
            'dataIndex': 'added_at',
            'width': 160
        }, {
            'text': 'Кем создано',
            'dataIndex': 'added_by_user'
        }]
    }, {
        'dataIndex': 'version',
        'width': 70
    }, {
        'dataIndex': 'completion_date',
        'width': 200,
    }, {
        'dataIndex': 'number',
        'width': 150,
    }, {
        'dataIndex': 'previous_insurer',
        'width': 150
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
            'filter': {'type': 'related', 'model': 'dict.pensionschemeops'},
            'width': 160,
        }]
    }, {
        'text': 'Застрахованное лицо',
        'columns': [{
            'text': 'ФИО',
            'columns': [{
                'dataIndex': 'person_last_name',
                'width': 105
            }, {
                'dataIndex': 'person_first_name',
                'width': 105
            }, {
                'dataIndex': 'person_middle_name',
                'width': 110
            }]
        }, {
            'text': 'ФИО при рождении',
            'columns': [{
                'text': 'Фамилия',
                'dataIndex': 'person_birth_last_name',
                'width': 105
            }, {
                'text': 'Имя',
                'dataIndex': 'person_birth_first_name',
                'width': 105
            }, {
                'text': 'Отчество',
                'dataIndex': 'person_birth_middle_name',
                'width': 110
            }]
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
        }, {
            'text': 'ССГПС',
            'dataIndex': 'person_insurance_certificate',
            'width': 200
        }]
    }]

    def get_list_filter(self, request):
        return self.fields

    def get_readonly_fields(self, request, obj=None):
        return self.fields

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class PersonOpsWorksheetAdmin(WorksheetAdmin):
    form = PersonOpsWorksheetForm
    model = Worksheet

    list_display = [
        'completion_date', 'version', 'state', 'number', 'previous_insurer', 'person_last_name', 'person_first_name',
        'person_middle_name', 'person_sex', 'person_birth_date', 'person_birth_place__street', 'person_nationality',
        'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
        'person_registered_address__index', 'person_registered_address__street', 'person_registered_address__house',
        'person_registered_address__corps', 'person_registered_address__apartment', 'person_insurance_certificate',
        'start_payment_date', 'end_payment_date', 'contribution_period', 'regular_payment', 'pension_scheme',
        'added_at', 'added_by_user']

    list_filter = [
        'completion_date', 'version', 'number', 'previous_insurer', WorksheetStateFilter, 'person_last_name',
        'person_first_name', 'person_middle_name', 'person_sex', 'person_birth_date', 'person_birth_place__street',
        'person_nationality', 'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
        'person_registered_address__index', 'person_registered_address__street', 'person_registered_address__house',
        'person_registered_address__corps', 'person_registered_address__apartment', 'person_insurance_certificate',
        'start_payment_date', 'end_payment_date', 'contribution_period', 'regular_payment', 'pension_scheme',
        'added_at', 'added_by_user']

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
        'dataIndex': 'previous_insurer',
        'width': 150
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
            'filter': {'type': 'related', 'model': 'dict.pensionschemeops'},
            'width': 160
        }]

    }, {
        'text': 'Застрахованное лицо',
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
        }, {
            'text': 'ССГПС',
            'dataIndex': 'person_insurance_certificate',
            'width': 200
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

    def get_inline_instances(self, request, obj=None):
        self.inlines = []
        if obj and obj.version > 0:
            self.inlines.append(WorksheetInputHistoryInline)
        return super().get_inline_instances(request, obj)

    def get_fieldsets(self, request, obj=None):
        none_fields = ['completion_date', 'file']

        person_fields = [
            'previous_insurer', 'person_birth_last_name', 'person_birth_first_name', 'person_birth_middle_name',
            'person_last_name', 'person_last_name_not_changed', 'person_first_name', 'person_first_name_not_changed',
            'person_middle_name', 'person_middle_name_not_changed', 'person_birth_date', 'person_nationality',
            'person_birth_place__street', 'person_phone', 'person_email']

        person_postal_address_fields = []

        if not obj:
            person_postal_address_fields += ['person_postal_address_same_as_registered_address']

        person_postal_address_fields += [
            'person_postal_address__index', 'person_postal_address__street', 'person_postal_address__house',
            'person_postal_address__corps', 'person_postal_address__apartment']

        if obj:
            none_fields += ['state']

            person_fields = [
                'previous_insurer', 'person_birth_last_name', 'person_birth_first_name', 'person_birth_middle_name',
                'person_last_name', 'person_first_name', 'person_middle_name', 'person_sex', 'person_birth_date',
                'person_nationality', 'person_birth_place__street', 'person_phone', 'person_email']

        return (
            (None, {'fields': none_fields}),
            ('Застрахованное лицо', {'fields': person_fields}),
            ('Адрес места жительтсва (регистрации)', {'fields': [
                'person_registered_address__index', 'person_registered_address__street',
                'person_registered_address__house', 'person_registered_address__corps',
                'person_registered_address__apartment']}),
            ('Почтовый адрес', {'fields': person_postal_address_fields}),
            ('Паспорт', {'fields': [
                'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
                'person_passport_subdivision_code', 'person_passport_issued_by', 'person_passport_file']}),
            ('Страховое свидетельство гос. пенсионного страхования', {'fields': [
                'person_insurance_certificate', 'person_insurance_certificate_file']}),
            ('Регулярные взносы (не менее 5 лет)', {'fields': [
                'pension_scheme', 'contribution_period', 'start_payment_date', 'end_payment_date', 'regular_payment']}),
        )

    def commit_final_version_worksheet(self, request, obj: Worksheet):
        """
        Подтверждение финальной версии анкеты и создание договора
        """
        if obj.number:
            return

        year = datetime.now().strftime('%y')

        # Присвоение номера договора
        obj.number = Api('0002-{counter_zl_' + year + '}/' + year).generate()
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
