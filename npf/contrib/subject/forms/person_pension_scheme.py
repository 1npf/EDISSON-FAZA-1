from django import forms

from npf.contrib.subject.models import PersonPensionScheme


class PersonPensionSchemeForm(forms.ModelForm):
    class Meta:
        model = PersonPensionScheme
        fields = '__all__'
