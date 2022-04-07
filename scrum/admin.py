from django.contrib import admin

from .models import (
    Developer,
    Project,
    TaskWorkload,
    TaskStatusName,
    Task,
    TaskStatusUpdateHistory,
)

admin.site.register(Developer)
admin.site.register(Project)
admin.site.register(TaskWorkload)
admin.site.register(TaskStatusName)
admin.site.register(Task)
admin.site.register(TaskStatusUpdateHistory)
