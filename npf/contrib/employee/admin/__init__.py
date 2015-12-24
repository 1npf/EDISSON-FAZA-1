from django.contrib import admin

from ..models import Department, Employee
from .department import DepartmentAdmin
from .employee import EmployeeAdmin

admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)