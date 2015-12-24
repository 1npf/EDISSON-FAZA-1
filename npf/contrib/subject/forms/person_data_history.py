from django import forms
from django.core import validators

from npf.contrib.subject.models import PersonDataHistory


class PersonDataHistoryForm(forms.ModelForm):

    class Meta:
        model = PersonDataHistory
        fields = '__all__'

    passport__series = forms.CharField(
        label='Серия', min_length=4, max_length=5, required=False,
        validators=[
            validators.RegexValidator(r'^\d{4}$|^\d{2}\s\d{2}$', 'Укажите корректную серию паспорта.', 'invalid')
        ]
    )

    passport__number = forms.CharField(
        label='Номер', min_length=6, max_length=6, required=False,
        validators=[
            validators.RegexValidator(r'^\d{6}$', 'Укажите корректный номер паспорта.', 'invalid')
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.passport:
            self.fields['passport__series'].initial = self.instance.passport.series
            self.fields['passport__number'].initial = self.instance.passport.number

    def save(self, commit=True):
        obj = super().save(commit)

        changed_fields = []

        if obj.passport and 'passport__series' in self.changed_data:
            obj.passport.series = self.cleaned_data['passport__series']
            changed_fields.append('series')

        if obj.passport and 'passport__number' in self.changed_data:
            obj.passport.number = self.cleaned_data['passport__number']
            changed_fields.append('number')

        if changed_fields:
            obj.passport.save(update_fields=changed_fields)

        return obj