
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from .project import Project


class UserGuiPreferences(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    selected_project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"(User='{self.user.name}', selected_project='{self.selected_project.name}')"


class UserNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    content = models.TextField(blank=True, default='')
    created_at = models.DateField(default=timezone.now, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.id}: {self.title}"
