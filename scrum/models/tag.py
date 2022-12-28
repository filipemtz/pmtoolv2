
from __future__ import annotations
from typing import List, Tuple
from django.db import models
from django.utils import timezone
from .project import Project
from .task_list import Task


class Tag(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=16)
    text_color = models.CharField(max_length=16)
    created_at = models.DateTimeField(default=timezone.now)

    @classmethod
    def extract_tags(cls, text: str) -> Tuple[List[str], str]:
        tags = []
        words = []

        for w in text.strip().split():
            w = w.strip()
            if (len(w) >= 2) and (w[0] == '#'):
                tag = w[1:]
                if len(tag) > 0:
                    tags.append(tag)
            else:
                words.append(w)

        text_without_tags = ' '.join(words)

        return tags, text_without_tags

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class TaskTag(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"({self.task.name}, {self.tag.name})"

    class Meta:
        ordering = ['-created_at']
