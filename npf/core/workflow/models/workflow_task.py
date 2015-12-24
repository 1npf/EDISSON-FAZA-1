from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group
from django.db import models
from django.core.urlresolvers import reverse
from .script_command import ScriptCommand
from .workflow_process import WorkflowProcess, WorkflowProcessInstance
from django.contrib.sites.models import Site

class WorkflowTask(models.Model):
    class ActionType:
        INSERT = 'i'
        UPDATE = 'u'
        DELETE = 'd'
        CONTROL = 'c'
        CHOICES = (
            (INSERT, 'Ввод данных'),
            (UPDATE, 'Редактирование'),
            (DELETE, 'Удаление'),
            (CONTROL, 'Контроль')
        )

    name = models.CharField(verbose_name='Название задачи', max_length=255, blank=True, null=True)
    order = models.IntegerField(verbose_name='Последовательный номер')
    process = models.ForeignKey(WorkflowProcess, verbose_name='Рабочий процесс')
    content_type = models.ForeignKey(ContentType, verbose_name='Тип объекта')
    action_type = models.CharField(verbose_name='Тип действия', max_length=1, choices=ActionType.CHOICES)
    user_group = models.ForeignKey(Group, verbose_name='Группа пользователей')
    due_time = models.TimeField(verbose_name='Время на выполнение', blank=True, null=True)
    automatic_assignment = models.BooleanField(verbose_name='Автоматическое назначение', default=False)
    affects_to_system_date = models.BooleanField(verbose_name='Влияет на дату системы', default=False)
    after_close_command = models.ForeignKey(ScriptCommand, verbose_name='Комманда после завершении', null=True,
                                            blank=True)
    version = models.IntegerField(verbose_name='Версия')
    last_version = models.ForeignKey(to='WorkflowTask', verbose_name='Последняя версия', null=True, blank=True)

    class Meta:
        verbose_name = 'Шаблон задачи'
        verbose_name_plural = 'Справочник задач'
        unique_together = ('id', 'order', 'version')

    def __str__(self):
        return self.name


class WorkflowTaskInstance(models.Model):
    class State:
        OPEN = 'o'
        CLOSED = 'c'
        CHOICES = (
            (OPEN, 'Открыта'),
            (CLOSED, 'Закрыта'),
        )

    custom_fields = ['object_url']

    def object_url(self):
        return "http://" + Site.objects.get_current().domain + "/#" + reverse("admin:%s_%s_change" % (self.content_type.app_label, self.content_type.model),
                               args=(self.object_id,))

    def is_reassigned(self):
        return self.performer is not None and self.performer.groups.filter(pk=self.task.user_group.pk).exists()

    task = models.ForeignKey(WorkflowTask, verbose_name='Шаблон задачи')
    process = models.ForeignKey(WorkflowProcessInstance, verbose_name='Экземпляр рабочего процесса')
    performer = models.ForeignKey(User, verbose_name='Исполнитель', null=True, blank=True)
    state = models.CharField(verbose_name='Статус', max_length=1, choices=State.CHOICES, default=State.OPEN)
    due_date = models.DateTimeField(verbose_name='Срок исполнения', blank=True, null=True)
    opened_at = models.DateTimeField(verbose_name='Дата и время создания', blank=True, null=True)
    closed_at = models.DateTimeField(verbose_name='Дата и время завершения', blank=True, null=True)
    object_id = models.PositiveIntegerField(verbose_name='ID объекта', null=True, blank=True)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Все задачи'

    def __str__(self):
        return self.task.name
