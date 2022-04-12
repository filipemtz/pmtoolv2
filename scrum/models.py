from __future__ import annotations  # recursive type hints

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .src.utils import NamedEnum


class Project(models.Model):
    name = models.CharField(max_length=100)
    team = models.ManyToManyField(User)

    def __str__(self):
        return self.name


class TaskWorkload(models.TextChoices):
    SMALL_1 = 'S1', _('small (1)')
    SMALL_2 = 'S2', _('small (2)')
    SMALL_3 = 'S3', _('small (3)')
    SMALL_5 = 'S5', _('small (5)')
    MEDIUM_8 = 'M8', _('medium (8)')
    MEDIUM_13 = 'M13', _('medium (13)')
    MEDIUM_21 = 'M21', _('medium (21)')
    LARGE_34 = 'L34', _('large (34)')
    LARGE_55 = 'L55', _('large (55)')
    LARGE_89 = 'L89', _('large (89)')
    EPIC_144 = 'E144', _('epic (144)')


class TaskStatus(models.TextChoices):
    TODO = 'TD', _('TODO')
    IN_PROGRESS = 'IP', _('IN PROGRESS')
    IN_REVIEW = 'RV', _('IN REVIEW')
    DONE = 'DO', _('DONE')


class TaskList(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    archived = models.BooleanField()
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"(name={self.name}, created_at={self.created_at}, project={self.project}, start={self.start_date}, end={self.end_date})"


class Task(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField()  # low numbers indicate high priority
    workload = models.TextField(max_length=4, choices=TaskWorkload.choices)
    status = models.TextField(max_length=2, choices=TaskStatus.choices)
    placement = models.ForeignKey(TaskList, on_delete=models.CASCADE)

    @classmethod
    def highest_priority_task(cls):
        return Task.objects.order_by('priority').first()

    @classmethod
    def lowest_priority_task(cls):
        # The negative sign in front of "-pub_date" indicates descending order. Ascending order is implied.
        tasks = Task.objects.order_by('-priority').first()

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"(name='{self.name}', Priority='{self.priority}', Workload='{self.workload}')"
