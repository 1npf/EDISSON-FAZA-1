from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from npf.contrib.common.validators import DigitOnlyValidator


@deconstructible
class InsuranceCertificateValidator(DigitOnlyValidator):
    code = 'invalid'

    def __call__(self, value):
        super().__call__(value)

        if len(value) < 11:
            return

        ks = value[len(value)-2:]
        k = 0
        s = 0

        while k < 9:
            k += 1
            s += (10 - k) * int(value[k-1])

        k_ost = s % 101 if s % 101 != 100 else 0

        if k_ost != int(ks):
            raise ValidationError('Контрольная суммма ССГПС не верна!')