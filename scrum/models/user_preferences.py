
from django.db import models
from django.contrib.auth.models import User
from .project import Project


class UserGuiPreferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"(User='{self.user.name}', selected_project='{self.selected_project.name}')"
