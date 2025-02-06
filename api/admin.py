from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


class CustomAdminUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email')}),
	('Personal Info', {'fields': ('name', 'surname', 'patronymic')}),
	('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')})
    )

admin.site.register(models.EmployeeModel)
admin.site.register(models.AdminModel, CustomAdminUser)
admin.site.register(models.TaskModel)
admin.site.register(models.EmployeeTaskModel)
admin.site.register(models.TrackingTaskModel)
admin.site.register(models.PlotModel)
admin.site.register(models.ItemModel)
