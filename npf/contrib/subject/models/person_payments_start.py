from django.db import models


class PersonPaymentsStart(models.Model):

    class Meta:
        verbose_name = 'Начало выплаты пенсии'
        verbose_name_plural = 'Начало выплаты пенсии'
        db_table = 'subject_person_payment_start'

    person = models.OneToOneField(to='subject.Person', parent_link=True, blank=True, null=True)
    payments_start_date = models.DateField(verbose_name='Дата')

    def __str__(self):
        return str(self.payments_start_date)

    '''
    def save(self, *args, **kwargs):
        history = PersonStateHistory.objects.filter(person=self.person)
        if not history or list(history)[-1].state != 'pensioner':
            PersonStateHistory.objects.create(
                person=self.person,
                date=self.payments_start_date,
                state='pensioner',
                reason=PersonStateReason.objects.get(id=7),
                added_by_user=user,
                modified_by_user=user
            )
        super().save(*args, **kwargs)
    '''