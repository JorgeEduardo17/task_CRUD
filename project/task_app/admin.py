from django.contrib import admin
from task_app.models import TaskUser


@admin.register(TaskUser)
class TaskUserAdmin(admin.ModelAdmin):
    pass
