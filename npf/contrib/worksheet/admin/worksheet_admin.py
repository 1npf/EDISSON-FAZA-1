import json
from datetime import datetime

from django import forms
from django.db.models import Q, F, ObjectDoesNotExist
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.forms import ModelChoiceField, TypedChoiceField
from django.utils.encoding import smart_text
from dateutil.relativedelta import relativedelta

from npf.contrib.common.validators import MinLengthValidator, MaxLengthValidator
from npf.core.modelaudit.admin import AuditFieldsAdminMixin
from npf.contrib.subject.models import Person
from npf.contrib.worksheet.models import *
from npf.core.xmin.admin import XminAdmin, XminTabularInline
from npf.core.xmin.settings import XMIN_XTYPE_FORMFIELD_MAP
from npf.contrib.address.forms import AddressField
from npf.contrib.address.models import Street, House


class WorksheetForm(forms.ModelForm):

    class Meta:
        model = Worksheet
        fields = '__all__'

    required_fields = []

    person_birth_place__street = AddressField(label='Место рождения')

    person_registered_address__index = forms.IntegerField(label='Почтовый индекс',
                                                          validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    person_registered_address__street = AddressField(label='Улица')
    person_registered_address__house = forms.IntegerField(label='Дом')
    person_registered_address__corps = forms.CharField(label='Корпус', max_length=2)
    person_registered_address__apartment = forms.IntegerField(label='Квартира')

    person_postal_address_same_as_registered_address = forms.BooleanField(
        label='Совпадает с адресом регистрации', initial=True,
        help_text='Отметьте, если почтовый адрес совпадает с адресом регистрации')

    person_postal_address__index = forms.IntegerField(label='Почтовый индекс',
                                                      validators=[MinLengthValidator(6), MaxLengthValidator(6)])

    person_postal_address__street = AddressField(label='Улица')
    person_postal_address__house = forms.IntegerField(label='Дом')
    person_postal_address__corps = forms.CharField(label='Корпус', max_length=2)
    person_postal_address__apartment = forms.IntegerField(label='Квартира')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            try:
                self.fields[field].required = self.instance.version == 0 and field in self.required_fields
            except KeyError:
                pass

        postal_address_required = self.instance.version == 0 and not \
            (True if not self.data else self.data.get('person_postal_address_same_as_registered_address') == 'on')

        if self.instance.version == 0:
            self.fields['person_postal_address__index'].required = postal_address_required
            self.fields['person_postal_address__street'].required = postal_address_required
            self.fields['person_postal_address__house'].required = postal_address_required

        try:
            address = self.instance.person_birth_place
            self.fields['person_birth_place__street'].initial = address.street
        except (ObjectDoesNotExist, AttributeError):
            pass

        try:
            address = self.instance.person_registered_address
            self.fields['person_registered_address__index'].initial = address.index
            self.fields['person_registered_address__street'].initial = address.street
            self.fields['person_registered_address__house'].initial = address.house
            self.fields['person_registered_address__corps'].initial = address.corps
            self.fields['person_registered_address__apartment'].initial = address.apartment
        except (ObjectDoesNotExist, AttributeError):
            pass

        try:
            address = self.instance.person_postal_address
            self.fields['person_postal_address__index'].initial = address.index
            self.fields['person_postal_address__street'].initial = address.street
            self.fields['person_postal_address__house'].initial = address.house
            self.fields['person_postal_address__corps'].initial = address.corps
            self.fields['person_postal_address__apartment'].initial = address.apartment
        except (ObjectDoesNotExist, AttributeError):
            pass

    def save(self, commit=True):
        instance = super().save(commit)

        person_birth_place__street = self.cleaned_data.get('person_birth_place__street', None)

        person_registered_address__index = self.cleaned_data.get('person_registered_address__index', None)
        person_registered_address__street = self.cleaned_data.get('person_registered_address__street', None)
        person_registered_address__house = self.cleaned_data.get('person_registered_address__house', None)
        person_registered_address__corps = self.cleaned_data.get('person_registered_address__corps', None)
        person_registered_address__apartment = self.cleaned_data.get('person_registered_address__apartment', None)

        person_postal_address__index = self.cleaned_data.get('person_registered_address__index', None)
        person_postal_address__street = self.cleaned_data.get('person_registered_address__street', None)
        person_postal_address__house = self.cleaned_data.get('person_registered_address__house', None)
        person_postal_address__corps = self.cleaned_data.get('person_registered_address__corps', None)
        person_postal_address__apartment = self.cleaned_data.get('person_registered_address__apartment', None)

        person_postal_address_same_as_registered_address = self.cleaned_data\
            .get('person_postal_address_same_as_registered_address', True)

        if person_postal_address_same_as_registered_address:
            person_postal_address__index = person_registered_address__index
            person_postal_address__street = person_registered_address__street
            person_postal_address__house = person_registered_address__house
            person_postal_address__corps = person_registered_address__corps
            person_postal_address__apartment = person_registered_address__apartment

        if person_birth_place__street:
            try:
                person_birth_place = instance.person_birth_place
                person_birth_place.street = person_birth_place__street
                person_birth_place.save()
            except ObjectDoesNotExist:
                RelatedModel = instance._meta.get_field('person_birth_place').rel.to
                fields = {'street': person_birth_place__street}
                instance.person_birth_place = RelatedModel.objects.create(**fields)

        if person_registered_address__index and person_registered_address__street and person_registered_address__house:
            try:
                person_registered_address = instance.person_registered_address
                person_registered_address.index = person_registered_address__index
                person_registered_address.street = person_registered_address__street
                person_registered_address.house = person_registered_address__house
                person_registered_address.corps = person_registered_address__corps
                person_registered_address.apartment = person_registered_address__apartment
                person_registered_address.save()
            except ObjectDoesNotExist:
                RelatedModel = instance._meta.get_field('person_registered_address').rel.to
                fields = {
                    'index': person_registered_address__index,
                    'street': person_registered_address__street,
                    'house': person_registered_address__house,
                    'corps': person_registered_address__corps,
                    'apartment': person_registered_address__apartment
                }
                instance.person_registered_address = RelatedModel.objects.create(**fields)

        if person_postal_address__index and person_postal_address__street and person_postal_address__house:
            try:
                person_postal_address = instance.person_postal_address
                person_postal_address.index = person_postal_address__index
                person_postal_address.street = person_postal_address__street
                person_postal_address.house = person_postal_address__house
                person_postal_address.corps = person_postal_address__corps
                person_postal_address.apartment = person_postal_address__apartment
                person_postal_address.save()
            except (ObjectDoesNotExist, AttributeError):
                RelatedModel = instance._meta.get_field('person_registered_address').rel.to
                fields = {
                    'index': person_postal_address__index,
                    'street': person_postal_address__street,
                    'house': person_postal_address__house,
                    'corps': person_postal_address__corps,
                    'apartment': person_postal_address__apartment
                }
                instance.person_postal_address = RelatedModel.objects.create(**fields)

        return instance

    def clean(self):
        cleaned_data = super().clean()
        today = datetime.today().date()
        completion_date = cleaned_data.get('completion_date')
        start_payment_date = cleaned_data.get('start_payment_date')
        end_payment_date = cleaned_data.get('end_payment_date')
        person_birth_date = cleaned_data.get('person_birth_date')
        person_passport_issue_date = cleaned_data.get('person_passport_issue_date')

        if completion_date and start_payment_date and start_payment_date < completion_date:
            self.add_error('completion_date',
                           'Дата заполнения анкеты не может быть больше даты начала периода взносов.')
            self.add_error('start_payment_date',
                           'Дата начала периода взносов не может быть меньше даты заполнения анкеты')

        if end_payment_date and end_payment_date < today:
            self.add_error('end_payment_date', 'Дата окончания периода взносов не должна быть меньше текущей.')

        if start_payment_date and end_payment_date and start_payment_date > end_payment_date:
            self.add_error('start_payment_date', 'Дата начала периода взносов не может быть больше даты окончания.')

        if start_payment_date and end_payment_date and relativedelta(end_payment_date, start_payment_date).years < 5:
            self.add_error('start_payment_date', 'Период взносов не должен быть менее 5 лет.')
            self.add_error('end_payment_date', 'Период взносов не должен быть менее 5 лет.')

        if person_birth_date and person_passport_issue_date and person_birth_date >= person_passport_issue_date:
            self.add_error('person_birth_date', 'Дата рождения не может быть больше либо равна дате выдачи паспорта.')
            self.add_error('person_passport_issue_date',
                           'Дата выдачи паспорта не может быть меньше либо равна дате рождения.')

        if person_passport_issue_date and person_passport_issue_date > today:
            self.add_error('person_passport_issue_date', 'Дата выдачи паспорта не может быть больше текущей даты')

        return cleaned_data


class CorrectionDataForm(forms.ModelForm):

    class Meta:
        model = CorrectionData
        fields = '__all__'

    worksheet_form = WorksheetForm

    def clean(self):
        cleaned_data = super().clean()
        field = cleaned_data.get('field')
        first_value = cleaned_data.get('first_value')
        second_value = cleaned_data.get('second_value')
        worksheet = cleaned_data.get('worksheet')

        check_fields_exclude = ['person_postal_address_same_as_registered_address']

        if first_value != second_value:
            msg = 'Значения первого и второго ввода не совпадают!'
            self.add_error('first_value', msg)
            self.add_error('second_value', msg)

        elif first_value == second_value:
            data = {}
            fields = self.worksheet_form.base_fields

            for field_name in fields:
                if field_name in check_fields_exclude:
                    continue

                related_names = field_name.split('__')
                field_value = worksheet
                for related_name in related_names:
                    field_value = getattr(field_value, related_name) if field_value else None

                form_field = fields[field_name]

                try:
                    data[field_name] = str(field_value.pk) if isinstance(form_field, ModelChoiceField) \
                        else smart_text(field_value)
                except AttributeError:
                    pass

            data[field] = first_value

            form = self.worksheet_form(data)
            if not form.is_valid() and field in form.errors:
                self.add_error('first_value', form.errors[field])
                self.add_error('second_value', form.errors[field])


class CorrectionDataInline(XminTabularInline):

    verbose_name_plural = 'Коррекция данных'
    commit_unchanged_records = True
    model = CorrectionData
    form = CorrectionDataForm
    fields = ['xtype', 'field', 'label', 'first_value', 'first_value_display', 'second_value', 'second_value_display']
    readonly_fields = ['label']
    ordering = ['label']
    extra = 0

    columns = [{
        'dataIndex': 'label',
        'flex': 1,
        'sortable': False,
        'hideable': False,
        'draggable': False
    }, {
        'dataIndex': 'first_value',
        'flex': 1,
        'sortable': False,
        'hideable': False,
        'draggable': False
    }, {
        'dataIndex': 'second_value',
        'flex': 1,
        'sortable': False,
        'hideable': False,
        'draggable': False
    }]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class WorksheetStateFilter(admin.SimpleListFilter):

    title = 'Статус'
    parameter_name = 'state'

    def lookups(self, request, model_admin):
        return Worksheet.State.CHOICES

    def queryset(self, request, queryset):
        val = self.value()

        if val == Worksheet.State.WAIT_SECOND_INPUT:
            return queryset.filter(version=0)

        if val == Worksheet.State.WAIT_CORRECTION:
            return queryset.filter(version__in=[1, 2], number=None)

        if val == Worksheet.State.COMMIT:
            return queryset.filter(~Q(number=None))

        return queryset


class WorksheetAdmin(AuditFieldsAdminMixin, XminAdmin):

    form = WorksheetForm
    correction_data_inline = CorrectionDataInline

    @property
    def identity_fields(self):
        return ['person_passport_series', 'person_passport_number', 'person_passport_issue_date', 'person_last_name',
                'person_first_name', 'person_middle_name', 'person_birth_date', 'person_nationality_id']

    def get_queryset(self, request):
        return super().get_queryset(request)\
            .filter(version=F('current_version'), type=self.model.__name__)\
            .order_by('-version')

    def get_inline_instances(self, request, obj=None):
        if obj and obj.version == 2 and CorrectionData.objects.filter(worksheet_id=obj.id)[:1]:
            self.inlines.append(self.correction_data_inline)
        return super().get_inline_instances(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return super().get_readonly_fields(request, obj)
        return ['state', 'number', 'version', 'completion_date', 'file', 'person_last_name', 'person_first_name',
                'previous_insurer', 'person_birth_last_name', 'person_birth_first_name', 'person_birth_middle_name',
                'person_middle_name', 'person_birth_date', 'person_sex', 'person_nationality',
                'person_birth_place__street', 'person_registered_address', 'person_postal_address', 'person_phone',
                'person_email', 'person_passport_series', 'person_passport_number', 'person_passport_issue_date',
                'person_passport_subdivision_code', 'person_passport_issued_by', 'person_insurance_certificate',
                'person_registered_address__index', 'person_registered_address__street',
                'person_registered_address__house', 'person_registered_address__corps',
                'person_registered_address__apartment', 'person_postal_address__index', 'person_postal_address__street',
                'person_postal_address__house', 'person_postal_address__corps', 'person_postal_address__apartment',
                'person_insurance_certificate_file', 'person_passport_file', 'third_person_last_name',
                'third_person_first_name', 'third_person_middle_name', 'third_person_sex', 'third_person_birth_date',
                'third_person_nationality', 'third_person_birth_place__street', 'third_person_registered_address',
                'third_person_postal_address', 'third_person_phone', 'third_person_email', 'third_person_document_type',
                'third_person_document_series', 'third_person_document_number', 'third_person_document_issue_date',
                'third_person_document_subdivision_code', 'third_person_document_issued_by',
                'third_person_insurance_certificate', 'third_person_registered_address__index',
                'third_person_registered_address__street', 'third_person_registered_address__house',
                'third_person_registered_address__corps', 'third_person_registered_address__apartment',
                'third_person_document_file', 'third_person_postal_address__index',
                'third_person_postal_address__street', 'third_person_postal_address__house',
                'third_person_postal_address__corps', 'third_person_postal_address__apartment',
                'third_person_document_file', 'third_person_insurance_certificate_file', 'pension_scheme',
                'contribution_period', 'start_payment_date', 'end_payment_date', 'regular_payment',
                'transfer_rights_date']

    def has_delete_permission(self, request, obj=None):
        if obj and obj.version == 0:
            return True
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            actions.pop('delete_selected')
        return actions

    def state(self, obj):
        return obj.state_display
    state.short_description = 'Статус'

    def save_model(self, request, obj, form, change):
        obj.content_type = ContentType.objects.get_for_model(obj)

        if change:
            super().save_model(request, obj, form, change)
            return

        worksheet = self.__get_suitable_worksheet(obj)
        if not worksheet:
            super().save_model(request, obj, form, change)
            return

        obj.version = 2
        super().save_model(request, obj, form, change)

        correction_data = self.__make_worksheet_correction_data(obj, form, worksheet)

        if correction_data:
            # Сохранение корректировочных данных анкеты
            CorrectionData.objects.bulk_create(correction_data)
        else:
            # Подтверждение финальной версии анкеты, так как все поля совпадают
            self.commit_final_version_worksheet(request, obj)

        if worksheet.version == 0:
            Worksheet.objects.filter(pk=worksheet.pk).update(version=1)

        Worksheet.objects.filter(pk__in=[obj.pk, worksheet.pk]).update(object_id=obj.pk, current_version=obj.version)

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)

        obj = form.instance

        # Создание финальной версии анкеты в результате коррекции данных
        if change and formset.has_changed() and obj.version == 2 and issubclass(formset.model, CorrectionData):
            self.__create_final_version_worksheet(request, form, formset)

    def __make_worksheet_correction_data(self, obj, form, worksheet_prev_version):
        """
        Создание корректировочных данных для исправления ошибок в анкете
        """
        correction_data = []
        check_fields_exclude = ['file', 'person_passport_file', 'person_insurance_certificate_file',
                                'third_person_document_file', 'third_person_insurance_certificate_file',
                                'person_postal_address_same_as_registered_address', 
                                'third_person_postal_address_same_as_registered_address',
                                'person_last_name_not_changed',
                                'person_first_name_not_changed',
                                'person_middle_name_not_changed']

        for field in form.fields:
            if field in check_fields_exclude:
                continue

            related_names = field.split('__')

            first_value = obj
            first_value_display = None
            for related_name in related_names:
                first_value = getattr(first_value, related_name) if first_value else None

            second_value = worksheet_prev_version
            second_value_display = None
            for related_name in related_names:
                second_value = getattr(second_value, related_name) if second_value else None

            if first_value != second_value:
                form_field = form.fields[field]
                form_field_class_name = '{0}.{1}'.format(form_field.__module__, form_field.__class__.__name__)
                xtype = XMIN_XTYPE_FORMFIELD_MAP[form_field_class_name]

                if not isinstance(xtype, dict):
                    xtype = {'xtype': xtype}

                if isinstance(form_field, TypedChoiceField):
                    xtype.update({'choices': form_field.choices})
                elif isinstance(form_field, ModelChoiceField):
                    xtype.update({'model': smart_text(form_field.queryset.model._meta)})

                is_related_field = isinstance(form_field, ModelChoiceField)
                is_choices_field = isinstance(form_field, TypedChoiceField)

                if is_choices_field:
                    first_value_display = getattr(obj, 'get_{0}_display'.format(field))()
                    second_value_display = getattr(worksheet_prev_version, 'get_{0}_display'.format(field))()
                elif is_related_field:
                    first_value_display = smart_text(first_value)
                    first_value = first_value.pk
                    second_value_display = smart_text(second_value)
                    second_value = second_value.pk

                label = form_field.label

                if field.startswith('person_passport_'):
                    label = 'Паспорт Вкладчика: ' + label

                elif field.startswith('person_insurance_certificate'):
                    label = 'Страховое свидетельство Вкладчика: ' + label

                elif field.startswith('person_'):
                    label = 'Вкладчик: ' + label

                elif field.startswith('person_registered_address_'):
                    label = 'Адрес места жительства (регистрации) Вкладчика: ' + label

                elif field.startswith('person_postal_address_'):
                    label = 'Почтовый адрес Вкладчика: ' + label

                elif field.startswith('third_person_registered_address_'):
                    label = 'Адрес места жительства (регистрации) Участника: ' + label

                elif field.startswith('third_person_postal_address_'):
                    label = 'Почтовый адрес Участника: ' + label

                if field.startswith('third_person_document_'):
                    label = 'Документ удостоверяющий личность участника: ' + label

                elif field.startswith('third_person_insurance_certificate'):
                    label = 'Страховое свидетельство участника: ' + label

                elif field.startswith('third_person_'):
                    label = 'Участник: ' + label

                if field in ['start_payment_date', 'end_payment_date', 'transfer_rights_date', 'regular_payment',
                             'contribution_period', 'pension_scheme']:
                    label = 'Регулярные взносы: ' + label

                correction_data.append(CorrectionData(
                    xtype=json.dumps(xtype, ensure_ascii=False),
                    field=field,
                    label=label,
                    first_value=first_value,
                    first_value_display=first_value_display,
                    second_value=second_value,
                    second_value_display=second_value_display,
                    worksheet_id=obj.pk
                ))

        return correction_data

    def __create_final_version_worksheet(self, request, form, formset):
        """
        Создание финальной версии анкеты
        """
        obj = form.instance
        if obj.version < 2:
            return

        contract_type = ContentType.objects.get_for_model(obj)

        # Удаление промежуточных данных для корректировки анкеты
        CorrectionData.objects.filter(worksheet_id=obj.id).delete()

        # Создание финальной версии анкеты, копируя текущую
        obj.pk = None
        obj.version = 3
        obj.current_version = 3
        obj.added_by_user = request.user
        obj.modified_by_user = request.user

        # Копирование места рождения
        try:
            obj.person_birth_place.pk = None
            obj.person_birth_place.save()
            obj.person_birth_place_id = obj.person_birth_place.pk
        except AttributeError:
            pass

        # Копирование места жительства
        try:
            obj.person_registered_address.pk = None
            obj.person_registered_address.save()
            obj.person_registered_address_id = obj.person_registered_address.pk
        except AttributeError:
            pass

        # Копирование почтового адреса
        try:
            obj.person_postal_address.pk = None
            obj.person_postal_address.save()
            obj.person_postal_address_id = obj.person_postal_address.pk
        except AttributeError:
            pass

        obj.save()

        # Применение корректировок к финальной версии анкеты
        worksheet_update_fields = {
            'object_id': obj.pk,
        }

        person_birth_place_update_fields = {}
        person_registered_address_update_fields = {}
        person_postal_address_update_fields = {}

        for changed_obj, fields in formset.changed_objects:
            if changed_obj.field.startswith('person_birth_place__'):
                field = changed_obj.field.split('person_birth_place__')
                person_birth_place_update_fields[field[1]] = changed_obj.first_value
            elif changed_obj.field.startswith('person_registered_address__'):
                field = changed_obj.field.split('person_registered_address__')
                person_registered_address_update_fields[field[1]] = changed_obj.first_value
            elif changed_obj.field.startswith('person_postal_address__'):
                field = changed_obj.field.split('person_postal_address__')
                person_postal_address_update_fields[field[1]] = changed_obj.first_value
            else:
                worksheet_update_fields[changed_obj.field] = changed_obj.first_value

            if changed_obj.field == 'person_middle_name' and changed_obj.first_value[-3:] == 'вич':
                worksheet_update_fields['person_sex'] = Person.Sex.MALE
            elif changed_obj.field == 'person_middle_name' and changed_obj.first_value[-3:] == 'вна':
                worksheet_update_fields['person_sex'] = Person.Sex.FEMALE

            if changed_obj.field == 'third_person_middle_name' and changed_obj.first_value[-3:] == 'вич':
                worksheet_update_fields['third_person_sex'] = Person.Sex.MALE
            elif changed_obj.field == 'third_person_middle_name' and changed_obj.first_value[-3:] == 'вна':
                worksheet_update_fields['third_person_sex'] = Person.Sex.FEMALE

        Worksheet.objects.filter(pk=obj.pk).update(**worksheet_update_fields)

        if person_birth_place_update_fields:
            Street.objects.filter(pk=obj.person_birth_place.pk).update(**person_birth_place_update_fields)

        if person_registered_address_update_fields:
            House.objects.filter(pk=obj.person_registered_address.pk).update(**person_registered_address_update_fields)

        if person_postal_address_update_fields:
            House.objects.filter(pk=obj.person_postal_address.pk).update(**person_postal_address_update_fields)

        # Привязка предыдущих версий анкет к финальной версии
        Worksheet.objects.filter(content_type__pk=contract_type.id, object_id=obj.object_id)\
            .update(object_id=obj.pk, current_version=obj.version)

        # Чтение последней версии из БД c учетом примененных корректировок
        obj = Worksheet.objects.get(pk=obj.pk)

        # Подтверждение последней версии и создание договора
        self.commit_final_version_worksheet(request, obj)

    def __get_suitable_worksheet(self, obj):
        """
        Поиск подходящей анкеты для связывания
        """
        if obj.version != 0:
            return None

        worksheets = Worksheet.objects\
            .filter(completion_date=obj.completion_date, version=0, type=self.model.__name__)\
            .values(*['id'] + self.identity_fields)

        result = {}

        for worksheet in worksheets:
            matched_fields = 0

            for field in self.identity_fields:
                if getattr(obj, field) == worksheet[field]:
                    matched_fields += 1

            matched_percent = (matched_fields / len(self.identity_fields)) * 100

            if matched_percent > 75:
                result[worksheet['id']] = matched_percent

        if result:
            max_matched_percent = max(result.values())
            for worksheet_id, percent in result.items():
                if percent == max_matched_percent:
                    return Worksheet.objects.select_for_update().get(pk=worksheet_id)

        return None

    def commit_final_version_worksheet(self, request, obj: Worksheet):
        """
        Подтверждение финальной версии анкеты и создание договора
        """
        raise NotImplementedError