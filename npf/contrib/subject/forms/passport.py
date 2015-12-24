from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator

from npf.contrib.common.validators import DigitOnlyValidator
from npf.contrib.subject.models import PersonPassport


class PassportForm(forms.ModelForm):

    class Meta:
        model = PersonPassport
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['series'].validators += [MinLengthValidator(4), MaxLengthValidator(4), DigitOnlyValidator()]
        self.fields['number'].validators += [MaxLengthValidator(6), MaxLengthValidator(6), DigitOnlyValidator()]
