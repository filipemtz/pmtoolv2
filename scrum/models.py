
from django.db import models
from django.contrib.auth.models import User
from .src.utils import NamedEnum


class Developer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=100)
    team = models.ManyToManyField(Developer)

    def __str__(self):
        return self.name


class TaskWorkload(models.Model):
    name = models.CharField(max_length=30)
    value = models.SmallIntegerField()

    def __str__(self) -> str:
        return self.name


class TaskStatusName(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


class TaskPlacementEnum(NamedEnum):
    BACKLOG = 1
    SPRINT = 2


class Task(models.Model):
    name = models.CharField(max_length=200)
    observation = models.TextField(blank=True)
    priority = models.IntegerField()
    workload = models.ForeignKey(
        TaskWorkload,
        on_delete=models.SET_NULL,
        null=True
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        Developer, on_delete=models.SET_NULL, null=True)
    placement = models.SmallIntegerField()

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"Requirement(name='{self.name}', Priority='{self.priority}', Workload='{self.workload}')"


class TaskStatusUpdateHistory(models.Model):
    status = models.ForeignKey(
        TaskStatusName, on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(
        Developer, on_delete=models.SET_NULL, null=True)
    requirement = models.ForeignKey(Task, on_delete=models.CASCADE)
    update_time = models.DateTimeField()

    @classmethod
    def task_status(cls, task_id: int):
        # most recent status assigned to the task
        return cls.objects.filter(requirement__id=task_id).order_by('-update_time').first().status

    def __str__(self) -> str:
        return f"({self.requirement.name}, {self.status.name} ({self.status.id}), {self.update_time}, {self.updated_by.user.username})"
