from django import forms

from npf.contrib.subject.models import PersonBankInfo


class BankInfoForm(forms.ModelForm):

    class Meta:
        model = PersonBankInfo
        fields = '__all__'