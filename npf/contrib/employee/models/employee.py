from django.db import models
from django.contrib.auth.models import User

from npf.contrib.employee.models import Department


class Employee(models.Model):
    user = models.OneToOneField(User, null=False, blank=False)
    department = models.ForeignKey(Department, null=True, blank=True, related_name='employees')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        db_table = 'employee_employee'

    def __str__(self):
        return self.user.get_full_name() or self.user.username