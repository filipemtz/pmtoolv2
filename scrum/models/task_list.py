
from __future__ import annotations
from typing import List
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .project import Project


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
    EPIC_233 = 'E233', _('epic (233)')
    EPIC_377 = 'E377', _('epic (377)')

    @classmethod
    def as_int(cls, val) -> int:
        return int(val[1:])


class TaskStatus(models.TextChoices):
    TODO = 'TD', _('to do')
    IN_PROGRESS = 'IP', _('in progress')
    IN_REVIEW = 'RV', _('in review')
    DONE = 'DO', _('done')

    @classmethod
    def as_icon(cls, val: str) -> str:
        # icons from bootstrap. see https://icons.getbootstrap.com/
        mapper = {
            TaskStatus.TODO: "bi-circle",
            TaskStatus.IN_PROGRESS: "bi-circle-half",
            TaskStatus.IN_REVIEW: "bi-circle-fill",
            TaskStatus.DONE: "bi-check-circle-fill",
        }

        icon_name = mapper[val]
        icon_html = f" <i class='bi {icon_name}'></i>"
        return icon_html


class TaskListType(models.TextChoices):
    ROUTINE = 'RT', _('routine')
    BACKLOG = 'BL', _('backlog')
    SPRINT = 'SP', _('sprint')


class TaskListFeeling(models.TextChoices):
    SUPERB = 'SB', _('SUPERB')
    HAPPY = 'HP', _('HAPPY')
    REGULAR = 'RE', _('REGULAR')
    SAD = 'SD', _('SAD')
    ANGRY = 'AG', _('ANGRY')
    UNDEFINED = 'UN', _('UNDEFINED')

    @classmethod
    def as_int(cls, val: TaskListFeeling) -> int:
        mapper = {
            TaskListFeeling.SUPERB: 2,
            TaskListFeeling.HAPPY: 1,
            TaskListFeeling.REGULAR: 0,
            TaskListFeeling.SAD: -1,
            TaskListFeeling.ANGRY: -2,
            TaskListFeeling.UNDEFINED: 0,
        }

        return mapper[val[0]]

    @classmethod
    def as_emoji(cls, val: TaskListFeeling) -> str:
        mapper = {
            TaskListFeeling.SUPERB: "128525",
            TaskListFeeling.HAPPY: "128522",
            TaskListFeeling.REGULAR: "128528",
            TaskListFeeling.SAD: "128542",
            TaskListFeeling.ANGRY: "128545",
            TaskListFeeling.UNDEFINED: "128156",
        }

        return mapper[val[0]]


class TaskList(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    archived = models.BooleanField()
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    task_list_type = models.TextField(
        max_length=2,
        choices=TaskListType.choices,
        default=TaskListType.SPRINT)
    observation = models.TextField(blank=True, default='')
    feeling = models.TextField(
        max_length=2,
        choices=TaskListFeeling.choices,
        default=TaskListFeeling.UNDEFINED)

    class Meta:
        ordering = ['-created_at']

    def completed_tasks(self) -> List[Task]:
        return [t for t in self.task_set.all() if t.status == TaskStatus.DONE]

    def n_completed_tasks(self) -> int:
        return len(self.completed_tasks())

    def n_points_completed(self) -> int:
        return sum([TaskWorkload.as_int(t.workload) for t in self.completed_tasks()])

    def total_points(self):
        return sum([TaskWorkload.as_int(t.workload) for t in self.task_set.all()])

    def percentual_tasks_completed(self):
        n_tasks = self.task_set.count()
        if n_tasks == 0:
            return 0
        return int(100 * self.n_completed_tasks() / n_tasks)

    def percentual_points_completed(self):
        total = self.total_points()
        if total == 0:
            return 0
        return int(100 * self.n_points_completed() / total)

    def __str__(self):
        return f"(name={self.name}, created_at={self.created_at}, project={self.project}, start={self.start_date}, end={self.end_date})"


class Task(models.Model):
    name = models.CharField(max_length=100)
    priority = models.IntegerField()  # low numbers indicate high priority
    workload = models.TextField(max_length=4, choices=TaskWorkload.choices)
    status = models.TextField(max_length=2, choices=TaskStatus.choices)
    placement = models.ForeignKey(TaskList, on_delete=models.CASCADE)
    status_update = models.DateTimeField()
    observation = models.TextField(blank=True, default='')
    duration = models.IntegerField(default=0)
    start_date = models.DateField(default=timezone.now, blank=True)
    end_date = models.DateField(default=timezone.now, blank=True)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    @classmethod
    def highest_priority_task(cls):
        return Task.objects.order_by('priority').first()

    @classmethod
    def lowest_priority_task(cls):
        # The negative sign in front of "-pub_date" indicates descending order. Ascending order is implied.
        return Task.objects.order_by('-priority').first()

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"name='{self.name}' (Priority='{self.priority}', Workload='{self.workload}', list='{self.placement.name}')"
