from django.db.models import ObjectDoesNotExist
from django import forms

from npf.core.counter.api import Api
from npf.contrib.common.validators import MinLengthValidator, MaxLengthValidator
from npf.contrib.dict.models import PensionSchemeNpo
from npf.contrib.account.models import Account, ContractPersonNpo, Contract
from npf.contrib.subject.models import Person, PersonPassport, PersonInsuranceCertificate
from npf.contrib.worksheet.models import Worksheet, IdentityDocumentType
from npf.contrib.worksheet.admin import (WorksheetAdmin, WorksheetForm, WorksheetStateFilter, CorrectionDataForm,
                                         CorrectionDataInline)

from npf.core.xmin.admin import XminGenericTabularInline, getter_for_related_field
from npf.contrib.common.validators import DigitOnlyValidator, BirthCertificateSeriesValidator
from npf.contrib.address.forms import AddressField

from datetime import datetime


class ThirdPersonWorksheetForm(WorksheetForm):
    third_person_birth_place__street = AddressField(label='Место рождения')

    third_person_registered_address__index = forms.IntegerField(
        label='Почтовый индекс', validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    third_person_registered_address__street = AddressField(label='Улица')
    third_person_registered_address__house = forms.IntegerField(label='Дом')
    third_person_registered_address__corps = forms.CharField(label='Корпус', max_length=2)
    third_person_registered_address__apartment = forms.IntegerField(label='Квартира')

    third_person_postal_address_same_as_registered_address = forms.BooleanField(
        label='Совпадает с адресом регистрации', initial=True,
        help_text='Отметьте, если почтовый адрес совпадает с адресом регистрации')

    third_person_postal_address__index = forms.IntegerField(
        label='Почтовый индекс', validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    third_person_postal_address__street = AddressField(label='Улица')
    third_person_postal_address__house = forms.IntegerField(label='Дом')
    third_person_postal_address__corps = forms.CharField(label='Корпус', max_length=2)
    third_person_postal_address__apartment = forms.IntegerField(label='Квартира')

    required_fields = [
        'completion_date', 'pension_scheme', 'end_payment_date', 'start_payment_date', 'contribution_period',
        'regular_payment', 'third_person_document_subdivision_code', 'person_passport_subdivision_code',
        'person_passport_series', 'person_passport_number', 'person_passport_issued_by',
        'third_person_registered_address__index', 'third_person_registered_address__street',
        'third_person_registered_address__house', 'person_nationality', 'person_passport_issue_date',
        'person_birth_date', 'person_last_name', 'person_first_name',
        'person_middle_name', 'person_birth_place__street', 'third_person_birth_place__street',
        'person_registered_address__index', 'person_registered_address__street', 'person_registered_address__house',
        'third_person_last_name', 'third_person_first_name', 'third_person_middle_name', 'third_person_birth_date',
        'third_person_nationality', 'third_person_document_type', 'third_person_document_series',
        'third_person_document_number', 'third_person_document_issue_date', 'third_person_document_issued_by']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.fields['pension_scheme'].queryset = PensionSchemeNpo.objects.all()
        except KeyError:
            pass

        if self.data.get('third_person_document_type') == IdentityDocumentType.PASSPORT:
            self.fields['third_person_document_series'].validators = [
                MinLengthValidator(4), MaxLengthValidator(4), DigitOnlyValidator()
            ]

            self.fields['third_person_document_number'].validators = [
                MinLengthValidator(6), MaxLengthValidator(6), DigitOnlyValidator()
            ]

        elif self.data.get('third_person_document_type') == IdentityDocumentType.BIRTH_CERTIFICATE:
            self.fields['third_person_document_series'].validators = [
                MinLengthValidator(4), MaxLengthValidator(5), BirthCertificateSeriesValidator()
            ]

            self.fields['third_person_document_number'].validators = [
                MinLengthValidator(6), MaxLengthValidator(6), DigitOnlyValidator()
            ]

        try:
            address = self.instance.person_birth_place
            self.fields['third_person_birth_place__street'].initial = address.street
        except (ObjectDoesNotExist, AttributeError):
            pass

        try:
            address = self.instance.third_person_registered_address
            self.fields['third_person_registered_address__index'].initial = address.index
            self.fields['third_person_registered_address__street'].initial = address.street
            self.fields['third_person_registered_address__house'].initial = address.house
            self.fields['third_person_registered_address__corps'].initial = address.corps
            self.fields['third_person_registered_address__apartment'].initial = address.apartment
        except (ObjectDoesNotExist, AttributeError):
            pass

        try:
            address = self.instance.third_person_postal_address
            self.fields['third_person_postal_address__index'].initial = address.index
            self.fields['third_person_postal_address__street'].initial = address.street
            self.fields['third_person_postal_address__house'].initial = address.house
            self.fields['third_person_postal_address__corps'].initial = address.corps
            self.fields['third_person_postal_address__apartment'].initial = address.apartment
        except (ObjectDoesNotExist, AttributeError):
            pass

    def clean(self):
        cleaned_data = super().clean()
        today = datetime.today().date()
        person_passport_series = cleaned_data.get('person_passport_series')
        person_passport_number = cleaned_data.get('person_passport_number')
        person_passport_subdivision_code = cleaned_data.get('person_passport_subdivision_code')
        person_passport_issue_date = cleaned_data.get('person_passport_issue_date')
        third_person_document_type = cleaned_data.get('third_person_document_type')
        third_person_document_series = cleaned_data.get('third_person_document_series')
        third_person_document_number = cleaned_data.get('third_person_document_number')
        third_person_document_subdivision_code = cleaned_data.get('third_person_document_subdivision_code')
        third_person_document_issue_date = cleaned_data.get('third_person_document_issue_date')
        third_person_birth_date = cleaned_data.get('third_person_birth_date')

        if third_person_document_type == IdentityDocumentType.PASSPORT and not third_person_document_subdivision_code:
            self.add_error('third_person_document_subdivision_code', 'Обязательное поле')

        if third_person_document_issue_date and third_person_document_type == IdentityDocumentType.PASSPORT \
                and third_person_document_issue_date > today:

            self.add_error('third_person_document_issue_date', 'Дата выдачи паспорта не может быть больше текущей даты')

        elif third_person_document_issue_date and third_person_document_type == IdentityDocumentType.BIRTH_CERTIFICATE \
                and third_person_document_issue_date > today:

            self.add_error('third_person_document_issue_date',
                           'Дата выдачи свидетельства о рождении не может быть больше текущей даты')

        if third_person_birth_date and third_person_document_issue_date:
            if third_person_document_type == IdentityDocumentType.PASSPORT \
                    and third_person_birth_date >= third_person_document_issue_date:

                self.add_error('third_person_birth_date', 'Дата рождения не может быть больше даты выдачи паспорта')

                self.add_error('third_person_document_issue_date',
                               'Дата выдачи паспорта не может быть меньше либо равна дате рождения')

            elif third_person_document_type == IdentityDocumentType.BIRTH_CERTIFICATE \
                    and third_person_birth_date > third_person_document_issue_date:

                self.add_error('third_person_birth_date',
                               'Дата рождения не может быть больше даты выдачи свидетельства о рождении')

                self.add_error('third_person_document_issue_date',
                               'Дата выдачи свидетельства о рождении не может быть меньше даты рождения')

        if third_person_document_type == IdentityDocumentType.PASSPORT:
            if third_person_document_subdivision_code and person_passport_subdivision_code \
                    and third_person_document_subdivision_code == person_passport_subdivision_code \
                    and third_person_document_issue_date and person_passport_issue_date \
                    and third_person_document_issue_date == person_passport_issue_date \
                    and third_person_document_series and person_passport_series \
                    and third_person_document_series == person_passport_series \
                    and third_person_document_number and person_passport_number \
                    and third_person_document_number == person_passport_number:

                passport_error_message = 'Пасспортные данные Вкладчика и участника совпадают!'
                error_fields = ['third_person_document_subdivision_code', 'person_passport_subdivision_code',
                                'third_person_document_issue_date', 'person_passport_issue_date',
                                'third_person_document_series', 'person_passport_series',
                                'third_person_document_number', 'person_passport_number']

                for field in error_fields:
                    self.add_error(field, passport_error_message)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit)

        third_person_birth_place__street = self.cleaned_data.get('person_birth_place__street', None)

        third_person_registered_address__index = self.cleaned_data.get('third_person_registered_address__index', None)
        third_person_registered_address__street = self.cleaned_data.get('third_person_registered_address__street', None)
        third_person_registered_address__house = self.cleaned_data.get('third_person_registered_address__house', None)
        third_person_registered_address__corps = self.cleaned_data.get('third_person_registered_address__corps', None)
        third_person_registered_address__apartment = self.cleaned_data.get('third_person_registered_address__apartment',
                                                                           None)

        third_person_postal_address__index = self.cleaned_data.get('third_person_registered_address__index', None)
        third_person_postal_address__street = self.cleaned_data.get('third_person_registered_address__street', None)
        third_person_postal_address__house = self.cleaned_data.get('third_person_registered_address__house', None)
        third_person_postal_address__corps = self.cleaned_data.get('third_person_registered_address__corps', None)
        third_person_postal_address__apartment = self.cleaned_data.get('third_person_registered_address__apartment',
                                                                       None)

        third_person_postal_address_same_as_registered_address = self.cleaned_data\
            .get('third_person_postal_address_same_as_registered_address', True)

        if third_person_postal_address_same_as_registered_address:
            third_person_postal_address__index = third_person_registered_address__index
            third_person_postal_address__street = third_person_registered_address__street
            third_person_postal_address__house = third_person_registered_address__house
            third_person_postal_address__corps = third_person_registered_address__corps
            third_person_postal_address__apartment = third_person_registered_address__apartment

        if third_person_birth_place__street:
            try:
                third_person_birth_place = instance.third_person_birth_place
                third_person_birth_place.street = third_person_birth_place__street
                third_person_birth_place.save()
            except (ObjectDoesNotExist, AttributeError):
                RelatedModel = instance._meta.get_field('third_person_birth_place').rel.to
                fields = {'street': third_person_birth_place__street}
                instance.third_person_birth_place = RelatedModel.objects.create(**fields)

        if third_person_registered_address__index and third_person_registered_address__street \
                and third_person_registered_address__house:
            try:
                third_person_registered_address = instance.third_person_registered_address
                third_person_registered_address.index = third_person_registered_address__index
                third_person_registered_address.street = third_person_registered_address__street
                third_person_registered_address.house = third_person_registered_address__house
                third_person_registered_address.corps = third_person_registered_address__corps
                third_person_registered_address.apartment = third_person_registered_address__apartment
                third_person_registered_address.save()
            except (ObjectDoesNotExist, AttributeError):
                RelatedModel = instance._meta.get_field('third_person_registered_address').rel.to
                fields = {
                    'index': third_person_registered_address__index,
                    'street': third_person_registered_address__street,
                    'house': third_person_registered_address__house,
                    'corps': third_person_registered_address__corps,
                    'apartment': third_person_registered_address__apartment
                }
                instance.third_person_registered_address = RelatedModel.objects.create(**fields)

        if third_person_postal_address__index and third_person_postal_address__street \
                and third_person_postal_address__house:
            try:
                third_person_postal_address = instance.third_person_postal_address
                third_person_postal_address.index = third_person_postal_address__index
                third_person_postal_address.street = third_person_postal_address__street
                third_person_postal_address.house = third_person_postal_address__house
                third_person_postal_address.corps = third_person_postal_address__corps
                third_person_postal_address.apartment = third_person_postal_address__apartment
                third_person_postal_address.save()
            except (ObjectDoesNotExist, AttributeError):
                RelatedModel = instance._meta.get_field('third_person_registered_address').rel.to
                fields = {
                    'index': third_person_postal_address__index,
                    'street': third_person_postal_address__street,
                    'house': third_person_postal_address__house,
                    'corps': third_person_postal_address__corps,
                    'apartment': third_person_postal_address__apartment
                }
                instance.third_person_postal_address = RelatedModel.objects.create(**fields)

        return instance


class ThirdPersonCorrectionDataForm(CorrectionDataForm):
    worksheet_form = ThirdPersonWorksheetForm


class ThirdPersonCorrectionDataInline(CorrectionDataInline):
    form = ThirdPersonCorrectionDataForm


class WorksheetInputHistoryInline(XminGenericTabularInline):
    verbose_name_plural = 'История двойного ввода'
    model = Worksheet
    extra = 0

    fields = [
        'completion_date', 'version', 'number', 'person_last_name', 'person_first_name', 'person_middle_name',
        'person_sex', 'person_birth_date', 'person_birth_place__street', 'third_person_birth_place__street',
        'person_nationality', 'person_passport_series', 'person_phone', 'person_email', 'person_passport_number',
        'person_passport_issue_date', 'person_passport_subdivision_code', 'person_passport_issued_by',
        'person_registered_address__index', 'person_registered_address__street', 'person_registered_address__house',
        'person_registered_address__corps', 'person_registered_address__apartment', 'person_postal_address__index',
        'person_postal_address__street', 'person_postal_address__house', 'person_postal_address__corps',
        'person_postal_address__apartment', 'third_person_registered_address__index',
        'third_person_registered_address__street', 'third_person_registered_address__house',
        'third_person_registered_address__corps', 'third_person_registered_address__apartment',
        'third_person_postal_address__index', 'third_person_postal_address__street',
        'third_person_postal_address__house', 'third_person_postal_address__corps',
        'third_person_postal_address__apartment', 'third_person_last_name', 'third_person_first_name',
        'third_person_middle_name', 'third_person_sex', 'third_person_birth_place__street', 'third_person_birth_date',
        'third_person_nationality',
        'third_person_phone', 'third_person_email', 'third_person_document_type', 'third_person_document_series',
        'third_person_document_number', 'third_person_document_subdivision_code', 'third_person_document_issue_date',
        'third_person_insurance_certificate', 'start_payment_date', 'end_payment_date', 'contribution_period',
        'regular_payment', 'pension_scheme', 'transfer_rights_date', 'added_at', 'added_by_user']

    list_filter = [
        'completion_date', 'version', 'number', 'person_last_name', 'person_first_name', 'person_middle_name',
        'person_sex', 'person_birth_date', 'person_birth_place__street', 'third_person_birth_place__street',
        'person_nationality', 'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
        'third_person_last_name', 'person_registered_address__index', 'person_registered_address__street',
        'person_registered_address__house', 'person_registered_address__corps', 'person_registered_address__apartment',
        'person_postal_address__index', 'person_postal_address__street', 'person_postal_address__house',
        'person_postal_address__corps', 'person_postal_address__apartment', 'third_person_registered_address__index',
        'third_person_registered_address__street', 'third_person_registered_address__house',
        'third_person_registered_address__corps', 'third_person_registered_address__apartment',
        'third_person_postal_address__index', 'third_person_postal_address__street',
        'third_person_postal_address__house', 'third_person_postal_address__corps',
        'third_person_postal_address__apartment', 'third_person_first_name', 'third_person_middle_name',
        'third_person_sex', 'third_person_birth_place__street', 'third_person_birth_date', 'third_person_nationality',
        'third_person_document_type',
        'third_person_document_series', 'third_person_document_number', 'third_person_document_issue_date',
        'third_person_insurance_certificate', 'start_payment_date', 'end_payment_date', 'contribution_period',
        'regular_payment', 'pension_scheme', 'transfer_rights_date', 'added_at', 'added_by_user']

    # Место рождения Вкладчика

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
    # Место рождения Участника

    third_person_birth_place__street = getter_for_related_field('third_person_birth_place__street',
                                                                short_description='Место рождения')

    # Адрес места жительства (регистрации) Участника

    third_person_registered_address__index = getter_for_related_field('third_person_registered_address__index',
                                                                      short_description='Почтовый индекс')

    third_person_registered_address__street = getter_for_related_field('third_person_registered_address__street',
                                                                       short_description='Улица')

    third_person_registered_address__house = getter_for_related_field('third_person_registered_address__house',
                                                                      short_description='Дом')

    third_person_registered_address__corps = getter_for_related_field('third_person_registered_address__corps',
                                                                      short_description='Корпус')

    third_person_registered_address__apartment = getter_for_related_field('third_person_registered_address__apartment',
                                                                          short_description='Квартира')
    # Почтовый адрес Участника

    third_person_postal_address__index = getter_for_related_field('third_person_postal_address__index',
                                                                  short_description='Почтовый индекс')

    third_person_postal_address__street = getter_for_related_field('third_person_postal_address__street',
                                                                   short_description='Улица')

    third_person_postal_address__house = getter_for_related_field('third_person_postal_address__house',
                                                                  short_description='Дом')

    third_person_postal_address__corps = getter_for_related_field('third_person_postal_address__corps',
                                                                  short_description='Корпус')

    third_person_postal_address__apartment = getter_for_related_field('third_person_postal_address__apartment',
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
        'width': 170,
    }, {
        'dataIndex': 'number',
        'width': 120,
    }, {
        'text': 'Регулярные взносы',
        'columns': [{
            'dataIndex': 'start_payment_date'
        }, {
            'dataIndex': 'end_payment_date'
        }, {
            'text': 'Переодичность',
            'dataIndex': 'contribution_period',
            'width': 110
        }, {
            'dataIndex': 'regular_payment',
            'width': 180
        }, {
            'dataIndex': 'pension_scheme',
            'filter': {'type': 'related', 'model': 'dict.pensionschemenpo'},
            'width': 140
        }, {
            'dataIndex': 'transfer_rights_date',
            'width': 140
        }]
    }, {
        'text': 'Вкладчик',
        'columns': [{
            'dataIndex': 'person_last_name'
        }, {
            'dataIndex': 'person_first_name'
        }, {
            'dataIndex': 'person_middle_name'

        }, {
            'dataIndex': 'person_sex'
        }, {
            'dataIndex': 'person_birth_date',
            'width': 110
        }, {
            'dataIndex': 'person_nationality'
        }, {
            'dataIndex': 'person_birth_place__street',
            'width': 200,
            'filter': 'address'
        }, {
            'text': 'Контакты',
            'columns': [{
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
                'text': 'Почтовый адрес',
                'columns': [{
                    'dataIndex': 'person_postal_address__index',
                    'width': 110,
                    'filter': 'string'
                }, {
                    'dataIndex': 'person_postal_address__street',
                    'width': 350,
                    'filter': 'address'
                }, {
                    'dataIndex': 'person_postal_address__house',
                    'filter': 'string'
                }, {
                    'dataIndex': 'person_postal_address__corps',
                    'filter': 'string'
                }, {
                    'dataIndex': 'person_postal_address__apartment',
                    'filter': 'string'
                }]
            }, {
                'dataIndex': 'person_phone',
                'width': 150
            }, {
                'dataIndex': 'person_email',
                'width': 200
            }]
        }, {
            'text': 'Паспорт',
            'columns': [{
                'dataIndex': 'person_passport_series'
            }, {
                'dataIndex': 'person_passport_number'
            }, {
                'dataIndex': 'person_passport_issue_date'
            }, {
                'dataIndex': 'person_passport_subdivision_code',
                'width': 150
            }, {
                'dataIndex': 'person_passport_issued_by',
                'width': 200
            }]
        }]
    }, {
        'text': 'Участник',
        'columns': [{
            'dataIndex': 'third_person_last_name'
        }, {
            'dataIndex': 'third_person_first_name'
        }, {
            'dataIndex': 'third_person_middle_name'
        }, {
            'dataIndex': 'third_person_sex'
        }, {
            'dataIndex': 'third_person_birth_date',
            'width': 110
        }, {
            'dataIndex': 'third_person_nationality'
        }, {
            'dataIndex': 'third_person_birth_place__street',
            'width': 200,
            'filter': 'address'
        }, {
            'text': 'Контакты',
            'columns': [{
                'text': 'Адрес места жительства (регистрации)',
                'columns': [{
                    'dataIndex': 'third_person_registered_address__index',
                    'width': 110,
                    'filter': 'string'
                }, {
                    'dataIndex': 'third_person_registered_address__street',
                    'width': 350,
                    'filter': 'address'
                }, {
                    'dataIndex': 'third_person_registered_address__house',
                    'filter': 'string'
                }, {
                    'dataIndex': 'third_person_registered_address__corps',
                    'filter': 'string'
                }, {
                    'dataIndex': 'third_person_registered_address__apartment',
                    'filter': 'string'
                }]
            }, {
                'text': 'Почтовый адрес',
                'columns': [{
                    'dataIndex': 'third_person_postal_address__index',
                    'width': 110,
                    'filter': 'string'
                }, {
                    'dataIndex': 'third_person_postal_address__street',
                    'width': 350,
                    'filter': 'address'
                }, {
                    'dataIndex': 'third_person_postal_address__house',
                    'filter': 'string'
                }, {
                    'dataIndex': 'third_person_postal_address__corps',
                    'filter': 'string'
                }, {
                    'dataIndex': 'third_person_postal_address__apartment',
                    'filter': 'string'
                }]
            }, {
                'dataIndex': 'third_person_phone',
                'width': 150
            }, {
                'dataIndex': 'third_person_email',
                'width': 200
            }]
        }, {
            'text': 'Документ удостоверяющий личность',
            'columns': [{
                'text': 'Тип',
                'dataIndex': 'third_person_document_type',
                'width': 200
            }, {
                'dataIndex': 'third_person_document_series'
            }, {
                'dataIndex': 'third_person_document_number'
            }, {
                'dataIndex': 'third_person_document_issue_date'
            }, {
                'dataIndex': 'third_person_document_subdivision_code',
                'width': 150
            }]
        }, {
            'text': 'ССГПС',
            'dataIndex': 'third_person_insurance_certificate',
            'width': 130
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


class ThirdPersonNpoWorksheetAdmin(WorksheetAdmin):

    form = ThirdPersonWorksheetForm
    correction_data_inline = ThirdPersonCorrectionDataInline

    list_display = [
        'completion_date', 'version', 'state', 'number', 'person_last_name', 'person_first_name', 'person_middle_name',
        'person_sex', 'person_birth_date', 'person_birth_place__street', 'third_person_birth_place__street',
        'person_nationality', 'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
        'third_person_last_name', 'third_person_first_name', 'person_registered_address__index',
        'person_registered_address__street', 'person_registered_address__house', 'person_registered_address__corps',
        'person_registered_address__apartment', 'third_person_registered_address__index',
        'third_person_registered_address__street', 'third_person_registered_address__house',
        'third_person_registered_address__corps', 'third_person_registered_address__apartment',
        'third_person_middle_name', 'third_person_sex', 'third_person_birth_date', 'third_person_nationality',
        'third_person_document_type', 'third_person_document_series', 'third_person_document_number',
        'third_person_document_issue_date', 'third_person_insurance_certificate', 'start_payment_date',
        'end_payment_date', 'contribution_period', 'regular_payment', 'pension_scheme', 'transfer_rights_date',
        'added_at', 'added_by_user']

    list_filter = [
        'completion_date', 'version', 'number', WorksheetStateFilter, 'person_last_name', 'person_first_name',
        'person_middle_name', 'person_sex', 'person_birth_date', 'person_birth_place__street',
        'third_person_birth_place__street', 'person_nationality', 'person_passport_series', 'person_passport_number',
        'person_passport_issue_date', 'third_person_last_name', 'person_registered_address__index',
        'person_registered_address__street', 'person_registered_address__house', 'person_registered_address__corps',
        'person_registered_address__apartment', 'third_person_registered_address__index',
        'third_person_registered_address__street', 'third_person_registered_address__house',
        'third_person_registered_address__corps', 'third_person_registered_address__apartment',
        'third_person_first_name', 'third_person_middle_name', 'third_person_sex', 'third_person_birth_date',
        'third_person_nationality', 'third_person_document_type', 'third_person_document_series',
        'third_person_document_number', 'third_person_document_issue_date', 'third_person_insurance_certificate',
        'start_payment_date', 'end_payment_date', 'contribution_period', 'regular_payment', 'pension_scheme',
        'transfer_rights_date', 'added_at', 'added_by_user']

    # Место рождения

    person_birth_place__street = getter_for_related_field('person_birth_place__street',
                                                          short_description='Место рождения')

    third_person_birth_place__street = getter_for_related_field('third_person_birth_place__street',
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

    person_postal_address__index = getter_for_related_field('person_registered_address__index',
                                                            short_description='Почтовый индекс')

    person_postal_address__street = getter_for_related_field('person_registered_address__street',
                                                             short_description='Улица')

    person_postal_address__house = getter_for_related_field('person_registered_address__house',
                                                            short_description='Дом')

    person_postal_address__corps = getter_for_related_field('person_registered_address__corps',
                                                            short_description='Корпус')

    person_postal_address__apartment = getter_for_related_field('person_registered_address__apartment',
                                                                short_description='Квартира')

    # Адрес места жительства (регистрации) Вкладчика

    third_person_registered_address__index = getter_for_related_field('third_person_registered_address__index',
                                                                      short_description='Почтовый индекс')

    third_person_registered_address__street = getter_for_related_field('third_person_registered_address__street',
                                                                       short_description='Улица')

    third_person_registered_address__house = getter_for_related_field('third_person_registered_address__house',
                                                                      short_description='Дом')

    third_person_registered_address__corps = getter_for_related_field('third_person_registered_address__corps',
                                                                      short_description='Корпус')

    third_person_registered_address__apartment = getter_for_related_field('third_person_registered_address__apartment',
                                                                          short_description='Квартира')

    # Почтовый адрес Вкладчика

    third_person_postal_address__index = getter_for_related_field('third_person_registered_address__index',
                                                                  short_description='Почтовый индекс')

    third_person_postal_address__street = getter_for_related_field('third_person_registered_address__street',
                                                                   short_description='Улица')

    third_person_postal_address__house = getter_for_related_field('third_person_registered_address__house',
                                                                  short_description='Дом')

    third_person_postal_address__corps = getter_for_related_field('third_person_registered_address__corps',
                                                                  short_description='Корпус')

    third_person_postal_address__apartment = getter_for_related_field('third_person_registered_address__apartment',
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
            'filter': {'type': 'related', 'model': 'dict.pensionschemenpo'},
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
        'text': 'Участник',
        'columns': [{
            'dataIndex': 'third_person_last_name',
            'width': 105
        }, {
            'dataIndex': 'third_person_first_name',
            'width': 105
        }, {
            'dataIndex': 'third_person_middle_name',
            'width': 110
        }, {
            'dataIndex': 'third_person_sex'
        }, {
            'dataIndex': 'third_person_birth_date',
            'width': 140
        }, {
            'dataIndex': 'third_person_birth_place',
            'width': 200
        }, {
            'dataIndex': 'third_person_nationality',
            'width': 200
        }, {
            'text': 'Адрес места жительства',
            'dataIndex': 'third_person_registered_address',
            'width': 350
        }, {
            'text': 'Адрес места жительства (регистрации)',
            'columns': [{
                'dataIndex': 'third_person_registered_address__index',
                'width': 110,
                'filter': 'string'
            }, {
                'dataIndex': 'third_person_registered_address__street',
                'width': 350,
                'filter': 'address'
            }, {
                'dataIndex': 'third_person_registered_address__house',
                'filter': 'string'
            }, {
                'dataIndex': 'third_person_registered_address__corps',
                'filter': 'string'
            }, {
                'dataIndex': 'third_person_registered_address__apartment',
                'filter': 'string'
            }]
        }, {
            'text': 'Документ удостоверяющий личность',
            'columns': [{
                'text': 'Тип',
                'dataIndex': 'third_person_document_type',
                'width': 200
            }, {
                'dataIndex': 'third_person_document_series'
            }, {
                'dataIndex': 'third_person_document_number'
            }, {
                'dataIndex': 'third_person_document_issue_date',
                'width': 130
            }]
        }, {
            'text': 'ССГПС',
            'dataIndex': 'third_person_insurance_certificate',
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

    @property
    def identity_fields(self):
        return ['person_passport_series', 'person_passport_number', 'person_passport_issue_date',
                'person_last_name', 'person_first_name', 'person_middle_name', 'person_birth_date',
                'person_nationality_id', 'third_person_document_series', 'third_person_document_number',
                'third_person_document_issue_date', 'third_person_last_name', 'third_person_first_name',
                'third_person_middle_name', 'third_person_birth_date', 'third_person_nationality_id']

    def get_inline_instances(self, request, obj=None):
        self.inlines = []
        if obj and obj.version > 0:
            self.inlines.append(WorksheetInputHistoryInline)
        return super().get_inline_instances(request, obj)

    def get_fieldsets(self, request, obj=None):
        none_fields = ['completion_date', 'file']

        person_fields = [
            'person_last_name', 'person_first_name', 'person_middle_name', 'person_birth_date', 'person_nationality',
            'person_birth_place__street', 'person_phone', 'person_email']

        third_person_fields = [
            'third_person_last_name', 'third_person_first_name', 'third_person_middle_name', 'third_person_birth_date',
            'third_person_nationality', 'third_person_birth_place__street', 'third_person_phone', 'third_person_email']

        if obj:
            none_fields += ['state']

            person_fields = ['person_last_name', 'person_first_name', 'person_middle_name', 'person_sex',
                             'person_birth_date', 'person_nationality', 'person_birth_place__street',
                             'person_phone', 'person_email']

            third_person_fields = ['third_person_last_name', 'third_person_first_name', 'third_person_middle_name',
                                   'third_person_sex', 'third_person_birth_date', 'third_person_nationality',
                                   'third_person_birth_place__street',
                                   'third_person_phone', 'third_person_email']

            if obj.number:
                none_fields = ['number', 'completion_date']

        person_postal_address_fields = []

        if not obj:
            person_postal_address_fields += ['person_postal_address_same_as_registered_address']

        person_postal_address_fields += ['person_postal_address__index', 'person_postal_address__street',
                                         'person_postal_address__house', 'person_postal_address__corps',
                                         'person_postal_address__apartment']

        third_person_postal_address_fields = []

        if not obj:
            third_person_postal_address_fields += ['third_person_postal_address_same_as_registered_address']

        third_person_postal_address_fields += [
            'third_person_postal_address__index', 'third_person_postal_address__street',
            'third_person_postal_address__house', 'third_person_postal_address__corps',
            'third_person_postal_address__apartment']

        return (
            (None, {'fields': none_fields}),
            ('Вкладчик', {'fields': person_fields}),
            ('Адрес места жительства (регистрации) Вкладчика', {'fields': [
                'person_registered_address__index', 'person_registered_address__street',
                'person_registered_address__house', 'person_registered_address__corps',
                'person_registered_address__apartment']
            }),
            ('Почтовый адрес Вкладчика', {'fields': person_postal_address_fields}),
            ('Паспорт Вкладчика', {'fields': [
                'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
                'person_passport_subdivision_code', 'person_passport_issued_by', 'person_passport_file']}),
            ('Участник (3-е лицо)', {'fields': third_person_fields}),
            ('Адрес места жительства (регистрации) Участника', {'fields': [
                'third_person_registered_address__index', 'third_person_registered_address__street',
                'third_person_registered_address__house', 'third_person_registered_address__corps',
                'third_person_registered_address__apartment']
            }),
            ('Почтовый адрес Участника', {'fields': third_person_postal_address_fields}),
            ('Документ удостоверяющий личность Участника', {'fields': [
                'third_person_document_type', 'third_person_document_series', 'third_person_document_number',
                'third_person_document_issue_date', 'third_person_document_issued_by',
                'third_person_document_subdivision_code', 'third_person_document_file']
            }),
            ('Страховое свидетельство гос. пенсионного страхования', {'fields': [
                'third_person_insurance_certificate', 'third_person_insurance_certificate_file']
            }),
            ('Регулярные взносы (не менее 5 лет)', {'fields': [
                'pension_scheme', 'contribution_period', 'start_payment_date', 'end_payment_date', 'regular_payment',
                'transfer_rights_date']}),
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
            #birth_place=obj.person_birth_place,
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
                #birth_place=obj.person_birth_place,
                sex=obj.person_sex,
                email=obj.person_email,
                mobile_phone=obj.person_phone,
                nationality=obj.person_nationality,
                #registered_address=obj.person_registered_address,
                #postal_address=obj.person_postal_address,
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

        third_person = Person.objects.filter(
            last_name=obj.third_person_last_name,
            first_name=obj.third_person_first_name,
            middle_name=obj.third_person_middle_name,
            birth_date=obj.third_person_birth_date,
            #birth_place=obj.third_person_birth_place,
            sex=obj.third_person_sex,
            nationality=obj.third_person_nationality)

        if obj.third_person_document_type == IdentityDocumentType.PASSPORT:
            third_person = third_person.filter(
                passport__series=obj.third_person_document_series,
                passport__number=obj.third_person_document_number,
                passport__issue_date=obj.third_person_document_issue_date)[:1]

        elif obj.third_person_document_type == IdentityDocumentType.BIRTH_CERTIFICATE:
            third_person = third_person.filter(
                birth_certificate__series=obj.third_person_document_series,
                birth_certificate__number=obj.third_person_document_number,
                birth_certificate__issue_date=obj.third_person_document_issue_date)[:1]

        if not third_person:
            third_person = Person.objects.create(
                last_name=obj.third_person_last_name,
                first_name=obj.third_person_first_name,
                middle_name=obj.third_person_middle_name,
                birth_date=obj.third_person_birth_date,
                #birth_place=obj.third_person_birth_place,
                sex=obj.third_person_sex,
                email=obj.third_person_email,
                mobile_phone=obj.third_person_phone,
                nationality=obj.third_person_nationality,
                #registered_address=obj.third_person_registered_address,
                #postal_address=obj.third_person_postal_address,
                added_by_user=request.user,
                modified_by_user=request.user
            )

            if obj.third_person_document_type == IdentityDocumentType.PASSPORT:
                third_person.passport = PersonPassport.objects.create(
                    series=obj.third_person_document_series,
                    number=obj.third_person_document_number,
                    issue_date=obj.third_person_document_issue_date,
                    issued_by=obj.third_person_document_issued_by,
                    subdivision_code=obj.third_person_document_subdivision_code,
                    added_by_user=request.user,
                    modified_by_user=request.user,
                    person=third_person
                )

            elif obj.third_person_document_type == IdentityDocumentType.BIRTH_CERTIFICATE:
                PersonInsuranceCertificate.objects.create(
                    number=obj.third_person_insurance_certificate,
                    added_by_user=request.user,
                    modified_by_user=request.user,
                    person=third_person
                )

        else:
            third_person = third_person[0]

        account = Account.objects.create(
            number=obj.number,
            investor=person,
            participant=third_person,
            opened_at=obj.added_at,
            transfer_rights_date=obj.transfer_rights_date,
            state=Account.State.OPEN,
            type=Account.Type.CUMULATIVE,
            added_by_user=request.user,
            modified_by_user=request.user,
        )

        ContractPersonNpo.objects.create(
            account=account,
            state=Contract.State.CONCLUDED,
            conclusion_date=datetime.today().date(),
            pension_scheme=obj.pension_scheme,
            contribution_period=obj.contribution_period,
            regular_payment_percent=obj.regular_payment,
            start_payment_date=obj.start_payment_date,
            end_payment_date=obj.end_payment_date,
            added_by_user=request.user,
            modified_by_user=request.user,
        )
