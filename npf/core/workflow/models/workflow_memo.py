from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

from npf.contrib.common.validators import FutureOnlyValidator

from .workflow_process import WorkflowProcessInstance


class WorkflowMemo(models.Model):

    class Type:
        BUG = 'b'
        TASK = 't'
        IMPROVEMENT = 'i'
        CHOICES = (
            (BUG, 'Ошибка'),
            (TASK, 'Задача'),
            (IMPROVEMENT, 'Улучшение'),
        )

    class Status:
        OPENED = 'o'
        RESOLVED = 'r'
        CLOSED = 'c'
        CHOICES = (
            (OPENED, 'Открыта'),
            (RESOLVED, 'Выполнена'),
            (CLOSED, 'Закрыта'),
        )

    title = models.CharField('Заголовок', max_length=255)
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    due_date = models.DateTimeField('Срок исполнения', validators=[FutureOnlyValidator()])
    deadline = models.DateTimeField('Крайний срок исполнения', validators=[FutureOnlyValidator()],
                                    blank=True, null=True)
    why_critical = models.TextField('Почему данная задача является критической',
                                    blank=True, null=True)
    task_type = models.CharField('Характер задачи', max_length=1, choices=Type.CHOICES)
    status = models.CharField('Статус', max_length=1, choices=Status.CHOICES,
                              default=Status.OPENED)
    text = models.TextField('Текст задачи')
    estimation = models.CharField('Временная оценка', max_length=100, blank=True, null=True)
    employment_rate = models.PositiveIntegerField('Процент занятости исполнителя',
                                                  validators=[MaxValueValidator(100)])
    related_memos = models.ManyToManyField('self', verbose_name='Связанные задачи', blank=True)
    customer = models.ForeignKey(User, editable=False, blank=True, null=True)
    current_participant = models.ForeignKey('workflow.Participant', editable=False,
                                            blank=True, null=True, on_delete=models.SET_NULL)
    process_instance = models.ForeignKey(WorkflowProcessInstance, verbose_name='Рабочий процесс',
                                         blank=True, null=True)
    complete = models.BooleanField('Завершить', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Служебная записка'
        verbose_name_plural = 'Служебные записки'


class Participant(models.Model):

    class Role:
        OPERATOR = 'o'
        PERFORMER = 'p'
        CHOICES = (
            (OPERATOR, 'Оператор'),
            (PERFORMER, 'Исполнитель'),
        )

    memo = models.ForeignKey(WorkflowMemo, verbose_name='Записка')
    user = models.ForeignKey(User, verbose_name='Сотрудник')
    role = models.CharField('Роль', max_length=1, choices=Role.CHOICES)
    spent = models.PositiveIntegerField('Затраченное время', blank=True, null=True)
    incoming_date = models.DateTimeField('Дата поступления', blank=True, null=True)
    completion_date = models.DateTimeField('Дата завершения', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Attachment(models.Model):

    memo = models.ForeignKey(WorkflowMemo, verbose_name='Записка')
    document = models.FileField('Файл', blank=True)

    class Meta:
        verbose_name = 'Прикрепленный файл'
        verbose_name_plural = 'Прикрепленные файлы'
