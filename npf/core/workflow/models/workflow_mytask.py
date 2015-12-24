from npf.core.workflow.models import WorkflowTaskInstance

class WorkflowMyTaskInstance(WorkflowTaskInstance):
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Мои задачи'
        proxy = True
