from django import forms

from npf.contrib.subject.models import PersonPaymentsStart


class PersonPaymentsStartForm(forms.ModelForm):
    class Meta:
        model = PersonPaymentsStart
        fields = '__all__'
