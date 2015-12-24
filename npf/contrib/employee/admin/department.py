from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from npf.contrib.employee.models import Employee
from npf.core.xmin.admin import XminAdmin


class EmployeeInline(admin.TabularInline):
    model = Employee
    fields = ['user']
    extra = 0


class DepartmentAdmin(XminAdmin, MPTTModelAdmin):
    list_display = ['name']
    inlines = [EmployeeInline]