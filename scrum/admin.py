from django.contrib import admin

from .models import (
    Project,
    TaskList,
    Task,
    UserGuiPreferences
)

admin.site.register(Project)
admin.site.register(TaskList)
admin.site.register(Task)
admin.site.register(UserGuiPreferences)
