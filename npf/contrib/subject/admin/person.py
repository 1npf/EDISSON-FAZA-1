from django import forms
from django.contrib import admin

from npf.contrib.subject.forms import BirthCertificateForm, \
    PersonPaymentsStartForm, PersonPensionSchemeForm, BankInfoForm, PersonDataHistoryForm
from npf.contrib.subject.models import Person, PersonPassport, PersonInsuranceCertificate, PersonBirthCertificate, \
    PersonStateHistory, PersonDataHistory, PersonBankInfo, PersonPaymentsStart, PersonPensionScheme
from npf.contrib.account.models import Account
from npf.contrib.common.forms import RequiredInlineFormSet
from npf.core.modelaudit.admin import AuditFieldsAdminMixin
from npf.core.xmin.admin import XminAdmin, RelatedFieldAdminMixin, getter_for_related_field

from npf.contrib.address.forms import AddressField
from npf.contrib.address.models import Street, House
from django.db.models import Q, F, ObjectDoesNotExist

from npf.contrib.common.validators import MinLengthValidator, MaxLengthValidator

class PassportFormSet(RequiredInlineFormSet):
    def get_queryset(self):
        return super().get_queryset()[:1]


class PassportInline(admin.StackedInline):
    verbose_name_plural = 'Паспорт'
    model = PersonPassport
    formset = PassportFormSet
    fields = ['series', 'number', 'subdivision_code', 'issue_date', 'issued_by', 'original']
    ordering = ['-id']
    max_num = 1

    def get_extra(self, request, obj=None, **kwargs):
        return 0 if obj else 1


class AddressInline(admin.StackedInline):
    verbose_name_plural = 'Адрес регистрации'
    model = PersonDataHistory
    form = PersonDataHistoryForm
    fields = ['registered_address__index', 'registered_address__street', 'registered_address__house',
              'registered_address__corps', 'registered_address__apartment']
    max_num = 1


class PostalAddressInline(admin.StackedInline):
    verbose_name_plural = 'Адрес почты'
    model = PersonDataHistory
    form = PersonDataHistoryForm
    fields = ['postal_address__index',
              'postal_address__street', 'postal_address__house',
              'postal_address__corps', 'postal_address__apartment']
    max_num = 1


class BirthCertificateInline(admin.StackedInline):
    verbose_name_plural = 'Свидетельство о рождении'
    model = PersonBirthCertificate
    form = BirthCertificateForm
    fields = ['series', 'number', 'issue_date', 'issued_by', 'original']
    max_num = 1


class InsuranceCertificateInline(admin.StackedInline):
    verbose_name_plural = 'Страховое свидетельство гос. пенсионного страхования'
    model = PersonInsuranceCertificate
    fields = ['number', 'original']
    max_num = 1
    extra = 1


class PersonStateHistoryInline(admin.TabularInline):
    verbose_name_plural = 'Статус'
    model = PersonStateHistory
    fields = ['date', 'state', 'reason']
    extra = 0


class PersonDataHistoryInline(RelatedFieldAdminMixin, admin.TabularInline):
    model = PersonDataHistory
    form = PersonDataHistoryForm

    fields = ['date', 'last_name', 'first_name', 'middle_name', 'sex', 'nationality']

    extra = 0

    def has_add_permission(self, request):
        return False

    #passport__series = getter_for_related_field('passport__series', short_description='Серия')
    #passport__number = getter_for_related_field('passport__number', short_description='Номер')


class AccountInlineFormSet(forms.BaseInlineFormSet):

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset


class AccountInline(admin.TabularInline):
    model = Account
    formset = AccountInlineFormSet
    fk_name = 'participant'
    extra = 0
    fields = ['number', 'added_at', 'opened_at', 'closed_at', 'transfer_rights_date', 'state', 'type', 'investor']
    readonly_fields = ['number', 'added_at', 'opened_at', 'closed_at', 'transfer_rights_date', 'state', 'type',
                       'investor']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


class PersonBankInfoInline(admin.StackedInline):
    verbose_name_plural = 'Банковские реквизиты'
    model = PersonBankInfo
    form = BankInfoForm
    fields = ['account', 'bank']


class PersonPaymentsStartInline(admin.StackedInline):
    model = PersonPaymentsStart
    form = PersonPaymentsStartForm
    fields = ['payments_start_date']


class PersonPensionSchemeInline(admin.StackedInline):
    model = PersonPensionScheme
    form = PersonPensionSchemeForm
    fields = ['pension_scheme']


class BirthPlaceForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = '__all__'

    birth_place__street = AddressField(label='Место рождения')

    registered_address__index = forms.IntegerField(label='Почтовый индекс',
                                                          validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    registered_address__street = AddressField(label='Улица')
    registered_address__house = forms.IntegerField(label='Дом')
    registered_address__corps = forms.CharField(label='Корпус', max_length=2, required=False)
    registered_address__apartment = forms.IntegerField(label='Квартира', required=False)

    postal_address__index = forms.IntegerField(label='Почтовый индекс',
                                                      validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    postal_address__street = AddressField(label='Улица')
    postal_address__house = forms.IntegerField(label='Дом')
    postal_address__corps = forms.CharField(label='Корпус', max_length=2, required=False)
    postal_address__apartment = forms.IntegerField(label='Квартира', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            address = self.instance.birth_place
            self.fields['birth_place__street'].initial = address.street
        except (ObjectDoesNotExist, AttributeError):
            pass

        try:
             address = self.instance.registered_address
             self.fields['registered_address__index'].initial = address.index
             self.fields['registered_address__street'].initial = address.street
             self.fields['registered_address__house'].initial = address.house
             self.fields['registered_address__corps'].initial = address.corps
             self.fields['registered_address__apartment'].initial = address.apartment
        except (ObjectDoesNotExist, AttributeError):
            pass
        try:
             address = self.instance.postal_address
             self.fields['postal_address__index'].initial = address.index
             self.fields['postal_address__street'].initial = address.street
             self.fields['postal_address__house'].initial = address.house
             self.fields['postal_address__corps'].initial = address.corps
             self.fields['postal_address__apartment'].initial = address.apartment
        except (ObjectDoesNotExist, AttributeError):
            pass

    def save(self, commit=True):
        instance = super().save(commit)

        birth_place__street = self.cleaned_data.get('birth_place__street', None)

        registered_address__index = self.cleaned_data.get('postal_address__index', None)
        registered_address__street = self.cleaned_data.get('registered_address__street', None)
        registered_address__house = self.cleaned_data.get('registered_address__house', None)
        registered_address__corps = self.cleaned_data.get('registered_address__corps', None)
        registered_address__apartment = self.cleaned_data.get('registered_address__apartment', None)

        postal_address__index = self.cleaned_data.get('postal_address__index', None)
        postal_address__street = self.cleaned_data.get('postal_address__street', None)
        postal_address__house = self.cleaned_data.get('postal_address__house', None)
        postal_address__corps = self.cleaned_data.get('postal_address__corps', None)
        postal_address__apartment = self.cleaned_data.get('postal_address__apartment', None)


        if birth_place__street:
            try:
                birth_place = instance.birth_place
                birth_place.street = birth_place__street
                birth_place.save()
            except ObjectDoesNotExist:
                RelatedModel = instance._meta.get_field('birth_place').rel.to
                fields = {'street': birth_place__street}
                instance.birth_place = RelatedModel.objects.create(**fields)

        if registered_address__index and registered_address__street and registered_address__house:
            try:
                registered_address = instance.registered_address
                registered_address.index = registered_address__index
                registered_address.street = registered_address__street
                registered_address.house = registered_address__house
                registered_address.corps = registered_address__corps
                registered_address.apartment = registered_address__apartment
                registered_address.save()
            except ObjectDoesNotExist:
                RelatedModel = instance._meta.get_field('registered_address').rel.to
                fields = {
                    'index': registered_address__index,
                    'street': registered_address__street,
                    'house': registered_address__house,
                    'corps': registered_address__corps,
                    'apartment': registered_address__apartment
                }
                instance.registered_address = RelatedModel.objects.create(**fields)

        if postal_address__index and postal_address__street and postal_address__house:
            try:
                postal_address = instance.postal_address
                #print postal_address
                if postal_address:
                    postal_address.index = postal_address__index
                    postal_address.street = postal_address__street
                    postal_address.house = postal_address__house
                    postal_address.corps = postal_address__corps
                    postal_address.apartment = postal_address__apartment
                    postal_address.save()
                else:
                    RelatedModel = instance._meta.get_field('postal_address').rel.to
                    fields = {
                        'index': postal_address__index,
                        'street': postal_address__street,
                        'house': postal_address__house,
                        'corps': postal_address__corps,
                        'apartment': postal_address__apartment
                    }
                    instance.postal_address = RelatedModel.objects.create(**fields)
            except ObjectDoesNotExist:
                RelatedModel = instance._meta.get_field('postal_address').rel.to
                fields = {
                    'index': postal_address__index,
                    'street': postal_address__street,
                    'house': postal_address__house,
                    'corps': postal_address__corps,
                    'apartment': postal_address__apartment
                }
                instance.postal_address = RelatedModel.objects.create(**fields)

        return instance

class PersonAdmin(AuditFieldsAdminMixin, XminAdmin):
    model = Person
    form = BirthPlaceForm

    required_fields = ['registered_address__street']

    list_display = ['id', 'name', 'last_name', 'first_name', 'middle_name', 'birth_date', 'sex',
                    'nationality', 'passport__series', 'passport__number', 'birth_place__street','registered_address__index', 'registered_address__street', 'registered_address__house',
                    'registered_address__corps', 'registered_address__apartment','postal_address__index', 'postal_address__street', 'postal_address__house',
                    'postal_address__corps', 'postal_address__apartment']

    search_fields = ['id', 'name', 'last_name', 'first_name', 'middle_name', 'birth_date', 'sex', 'passport__series',
                     'nationality__short_name', 'passport__number', 'birth_place__street','registered_address__index', 'registered_address__street', 'registered_address__house',
                     'registered_address__corps', 'registered_address__apartment','postal_address__index', 'postal_address__street', 'postal_address__house',
                     'postal_address__corps', 'postal_address__apartment']

    fieldsets = (
        (None, {'fields': ['last_name', 'first_name', 'middle_name',
                           'birth_date', 'sex', 'nationality', 'birth_place__street']}),
        ('Контакты', {'fields': ['email', 'mobile_phone', 'work_phone', 'home_phone']}),
        ('Адрес регистрации', {'fields': ['registered_address__index', 'registered_address__street', 'registered_address__house',
                                          'registered_address__corps', 'registered_address__apartment']}),
        ('Адрес почты', {'fields': ['postal_address__index', 'postal_address__street', 'postal_address__house',
                                    'postal_address__corps', 'postal_address__apartment']}),
    )

    inlines = (PassportInline, BirthCertificateInline, InsuranceCertificateInline, PersonDataHistoryInline,
               PersonStateHistoryInline, AccountInline, PersonBankInfoInline, PersonPaymentsStartInline,
               PersonPensionSchemeInline)

    passport__series = getter_for_related_field('passport__series', short_description='Серия')
    passport__number = getter_for_related_field('passport__number', short_description='Номер')
    birth_place__street = getter_for_related_field('birth_place__street', short_description='Номер')

    birth_place__street = AddressField(label='Место рождения')

    registered_address__index = forms.IntegerField(label='Почтовый индекс',
                                                   validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    registered_address__street = AddressField(label='Улица')
    registered_address__house = forms.IntegerField(label='Дом')
    registered_address__corps = forms.CharField(label='Корпус', max_length=2, required=False)
    registered_address__apartment = forms.IntegerField(label='Квартира', required=False)

    postal_address__index = forms.IntegerField(label='Почтовый индекс',
                                               validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    postal_address__street = AddressField(label='Улица')
    postal_address__house = forms.IntegerField(label='Дом')
    postal_address__corps = forms.CharField(label='Корпус', max_length=2, required=False)
    postal_address__apartment = forms.IntegerField(label='Квартира', required=False)


    columns =[{
            'dataIndex': 'last_name',
            'width': 105
        }, {
            'dataIndex': 'first_name',
            'width': 105
        }, {
            'dataIndex': 'middle_name',
            'width': 110
        }, {
            'dataIndex': 'sex'
        }, {
            'dataIndex': 'birth_date',
            'width': 140
        }, {
            'text': 'Адрес рождения',
            'dataIndex': 'birth_place__street',
            'width': 200,
            'filter': 'address'
        }, {
            'dataIndex': 'nationality',
            'width': 200
        }, {
            'text': 'Адрес места жительства (регистрации)',
            'columns': [{
                'text': 'Индекс',
                'dataIndex': 'registered_address__index',
                'width': 110,
                'filter': 'string'
            }, {
                'text': 'Улица',
                'dataIndex': 'registered_address__street',
                'width': 350,
                'filter': 'address'
            }, {
                'text': 'Дом',
                'dataIndex': 'registered_address__house',
                'width': 350,
                'filter': 'string'
            }, {
                'text': 'Корпус',
                'dataIndex': 'registered_address__corps',
                'width': 350,
                'filter': 'string'
            }, {
                'text': 'Квартира',
                'dataIndex': 'registered_address__apartment',
                'width': 350,
                'filter': 'string'
            }]
        }, {
            'text': 'Паспорт',
            'columns': [{
                'text': 'Серия паспорта',
                'dataIndex': 'passport_series'
            }, {
                'text': 'Номер паспорта',
                'dataIndex': 'passport_number'
            }, {
                'text': 'Дата выдачи паспорта',
                'dataIndex': 'passport_issue_date',
                'width': 130
            }]
        }, {
            'dataIndex': 'email',
            'width': 105
        }, {
            'dataIndex': 'mobile_phone',
            'width': 105
        }, {
            'dataIndex': 'work_phone',
            'width': 105
        }, {
            'dataIndex': 'home_phone',
            'width': 105
        }]

    def save_model(self, request, obj, form, change):
        obj.first_name = obj.first_name.capitalize()
        obj.last_name = obj.last_name.capitalize()

        obj.middle_name = obj.middle_name.capitalize()
        obj.name = '{0} {1}.{2}.'.format(obj.last_name, obj.first_name[:1], obj.middle_name[:1])

        if change:
            request._old_obj = Person.objects.select_for_update().get(pk=obj.pk)
            request._old_passport = request._old_obj.passport

            if form.has_changed():
                # save old person data
                PersonDataHistory.objects.create(
                    person=obj,
                    date=request._old_obj.modified_at.date(),
                    last_name=request._old_obj.last_name,
                    first_name=request._old_obj.first_name,
                    middle_name=request._old_obj.middle_name,
                    sex=request._old_obj.sex,
                    nationality=request._old_obj.nationality,
                    #registered_address=request._old_obj.registered_address,
                    #postal_address=request._old_obj.postal_address,
                    added_by_user=request.user,
                    modified_by_user=request.user,
                    passport=request._old_passport,
                )

        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)

        obj = form.instance

        if issubclass(formset.model, PersonPassport):
            if change and formset.has_changed():
                if not form.has_changed():
                    # save old person data
                    PersonDataHistory.objects.create(
                        person=obj,
                        date=request._old_obj.modified_at.date(),
                        last_name=request._old_obj.last_name,
                        first_name=request._old_obj.first_name,
                        middle_name=request._old_obj.middle_name,
                        sex=request._old_obj.sex,
                        nationality=request._old_obj.nationality,
                        #registered_address=request._old_obj.registered_address,
                        #postal_address=request._old_obj.postal_address,
                        added_by_user=request.user,
                        modified_by_user=request.user,
                        passport=request._old_passport,
                    )

                # revert saved passport
                request._old_passport.save()

                # save new passport
                passport = formset.changed_objects[0][0]

                form.instance.passport = PersonPassport.objects.create(
                    person=obj,
                    series=passport.series,
                    number=passport.number,
                    subdivision_code=passport.subdivision_code,
                    issue_date=passport.issue_date,
                    issued_by=passport.issued_by,
                    original=passport.original,
                    added_by_user=request.user,
                    modified_by_user=request.user,
                )

                form.instance.save(update_fields=['passport'])

            elif not change:
                form.instance.passport = formset.new_objects[0]
                form.instance.save(update_fields=['passport'])
