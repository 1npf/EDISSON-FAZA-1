from django import forms

from npf.contrib.account.models import ContractPersonNpo
from npf.contrib.subject.models import Person
from npf.core.xmin.admin import XminAdmin


class ContractCreationForm(forms.ModelForm):
    person = forms.ModelChoiceField(label='Вкладчик', queryset=Person.objects.all())
    third_person = forms.ModelChoiceField(label='Участник', queryset=Person.objects.all(), required=False,
                                          help_text='Оставьте поле пустым если Вкладчик и участник одно лицо')

    class Meta:
        model = ContractPersonNpo
        fields = ['person', 'conclusion_date']


class ContractEditionForm(forms.ModelForm):
    class Meta:
        model = ContractPersonNpo
        fields = ['account', 'conclusion_date', 'termination_date', 'state']


class ContractPersonNpoAdmin(XminAdmin):
    list_display = ['account', 'conclusion_date', 'termination_date', 'state']
    #fields = ['account', 'conclusion_date', 'termination_date', 'state']
    ordering = ['account__number']

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return ContractCreationForm
        return ContractEditionForm