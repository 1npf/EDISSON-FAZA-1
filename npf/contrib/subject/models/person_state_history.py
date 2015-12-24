from django.db import models

from npf.core.modelaudit.models import AuditFieldsMixin


class PersonState(object):
    INSURED = 'insured'
    DEPOSITOR = 'depositor'
    PARTICIPANT = 'participant'
    PENSIONER = 'pensioner'
    DIED = 'died'
    GONE = 'gone'
    CHOICES = (
        (INSURED, 'Застрахованное лицо'),
        (DEPOSITOR, 'Вкладчик'),
        (PARTICIPANT, 'Участник'),
        (PENSIONER, 'Пенсионер'),
        (DIED, 'Умер'),
        (GONE, 'Выбыл'),
    )
    MAP = {
        DEPOSITOR: (PENSIONER, DIED, GONE),
        PARTICIPANT: (DEPOSITOR, PENSIONER, DIED),
        PENSIONER: (DIED,),
        DIED: ()
    }


class PersonStateHistory(AuditFieldsMixin, models.Model):

    class Meta:
        verbose_name = 'Статус участника'
        verbose_name_plural = 'История состояний участника'
        db_table = 'subject_person_state_history'

    person = models.ForeignKey(to='subject.Person', verbose_name='Физическое лицо', related_name='states')
    date = models.DateField(verbose_name='Дата')
    state = models.CharField(verbose_name='Статус', max_length=11, choices=PersonState.CHOICES, db_index=True)
    reason = models.ForeignKey(to='dict.PersonStateReason', verbose_name='Основание')

    def __str__(self):
        return '{0} ({1})'.format(self.person.__str__(), self.get_state_display())