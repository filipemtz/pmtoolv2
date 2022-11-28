
from __future__ import annotations
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=100)
    team = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this book."""
        return reverse('project', args=[str(self.id)])
