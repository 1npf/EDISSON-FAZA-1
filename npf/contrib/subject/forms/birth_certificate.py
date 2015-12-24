from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator

from npf.contrib.common.validators import DigitOnlyValidator, BirthCertificateSeriesValidator
from npf.contrib.subject.models import PersonBirthCertificate


class BirthCertificateForm(forms.ModelForm):

    class Meta:
        model = PersonBirthCertificate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['series'].validators += [
            MinLengthValidator(4),
            MaxLengthValidator(4),
            BirthCertificateSeriesValidator()
        ]

        self.fields['number'].validators += [MinLengthValidator(6), MaxLengthValidator(6), DigitOnlyValidator()]