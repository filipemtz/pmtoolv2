from typing import Dict, List
from django.shortcuts import get_object_or_404, render
from django.template import loader
# Create your views here.
from django.http import HttpResponse
from .models import Project, Task, TaskStatusName, TaskStatusUpdateHistory, TaskWorkload


def task_view(task: Task) -> str:
    task_status = TaskStatusUpdateHistory.task_status(task.id)
    status_selector_html = status_selector(selected_value=task_status.id)
    workload_selector_html = workload_selector(selected_value=task.workload.id)

    task_html = loader.get_template('scrum/task.html').render({
        "task": task,
        "workload_selector_html": workload_selector_html,
        "status_selector_html": status_selector_html,
    })

    return task_html


def render_selector(options: List[Dict]) -> str:
    status_selector_html = loader.get_template('scrum/selector.html').render({
        "name": "status",
        "id": "status",
        "options": options,
    })
    return status_selector_html


def status_selector(selected_value: int = -1) -> str:
    all_status = TaskStatusName.objects.all()
    status_options = [{'name': s.name, 'value': s.id,
                       'selected': selected_value == s.id} for s in all_status]
    return render_selector(status_options)


def project_selector(selected_value: int = -1):
    all_objs = Project.objects.all()
    options = [{'name': o.name, 'value': o.id,
                'selected': selected_value == o.id} for o in all_objs]
    return render_selector(options)


def workload_selector(selected_value: int = -1):
    all_objs = TaskWorkload.objects.all()
    options = [{'name': o.name, 'value': o.id,
                'selected': selected_value == o.id} for o in all_objs]
    return render_selector(options)


def index(request):
    project_id = 1
    project = get_object_or_404(Project, pk=project_id)
    tasks = Task.objects.filter(project=project)
    tasks_html = [task_view(t) for t in tasks]
    project_html = project_selector(project_id)

    return render(request, 'scrum/index.html', {
        'project': project_html,
        'tasks': tasks_html,
    })
