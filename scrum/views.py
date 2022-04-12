import enum
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Project, Task, TaskList, TaskStatus, TaskWorkload
from django.views import View
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.shortcuts import get_object_or_404, render
from typing import Dict, List
import traceback


def render_task(task: Task) -> str:
    onselect_event = f"save_task({task.id});"
    status_selector_html = status_selector(
        selected_value=task.status, onselect_event=onselect_event)
    workload_selector_html = workload_selector(
        selected_value=task.workload, onselect_event=onselect_event)

    task_html = loader.get_template('scrum/task.html').render({
        "task": task,
        "workload_selector_html": workload_selector_html,
        "status_selector_html": status_selector_html,
    })

    return task_html


def render_selector(options: List[Dict], name: str, id, onselect_event: str = '') -> str:
    status_selector_html = loader.get_template('scrum/selector.html').render({
        "name": name,
        "id": id,
        "options": options,
        'onselect_event': onselect_event,
    })
    return status_selector_html


def status_selector(selected_value: str = '', onselect_event: str = '') -> str:
    all_status = TaskStatus.choices
    status_options = [{'name': s[1], 'value': s[0],
                       'selected': selected_value == s[0]} for s in all_status]
    return render_selector(status_options, name='status', id='status', onselect_event=onselect_event)


def project_selector(selected_value: int = -1):
    all_objs = Project.objects.all()
    options = [{'name': o.name, 'value': o.id,
                'selected': selected_value == o.id} for o in all_objs]
    onselect_event = "page_alert('multiproject is not implemented yet', INFO_CLASS, fadeOutTime = 2);"
    return render_selector(options, name='project', id='project', onselect_event=onselect_event)


def workload_selector(selected_value: str = '', onselect_event: str = ''):
    all_objs = TaskWorkload.choices
    options = [{'name': o[1], 'value': o[0],
                'selected': selected_value == o[0]} for o in all_objs]
    return render_selector(options, name='workload', id='workload', onselect_event=onselect_event)


def update_task(request):
    task = get_object_or_404(Task, id=request.POST['task_id'])
    task.name = request.POST['name']
    task.workload = request.POST['workload']
    task.status = request.POST['status']
    task.save()
    return HttpResponse(render_task(task))


def delete_task(request):
    task = Task.objects.get(id=request.POST['task_id'])
    task.delete()
    return HttpResponse()


def get_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    return HttpResponse(render_task(task))


def create_empty_task(request):
    task_list = get_object_or_404(TaskList, id=request.POST['task_list_id'])

    low_priority_task = Task.lowest_priority_task()
    if low_priority_task:
        priority = low_priority_task.priority + 1
    else:
        priority = 1

    task = Task(
        name='new task',
        priority=priority,
        workload=TaskWorkload.SMALL_1,
        status=TaskStatus.TODO,
        placement=task_list
    )

    task.save()

    return HttpResponse(render_task(task))


def render_task_list(task_list: TaskList, template: str) -> str:
    subtasks = Task.objects.filter(placement=task_list)
    subtasks_html = [render_task(t) for t in subtasks]
    task_list_html = loader.get_template(template).render({
        "task_list": task_list,
        "subtasks": subtasks_html,
    })
    return task_list_html


def extract_int_id(html_id):
    return int(html_id.split("_")[-1])


def update_priorities(request):
    if 'task_list_id' not in request.POST:
        return HttpResponseNotFound()

    task_list_id = request.POST['task_list_id']
    task_list_id = extract_int_id(task_list_id)
    task_list = TaskList.objects.get(id=task_list_id)

    sorted_tasks = request.POST.getlist('sorted_tasks[]')
    ids = [extract_int_id(s) for s in sorted_tasks]

    for i in range(len(ids)):
        task = Task.objects.get(id=ids[i])
        task.priority = i + 1
        task.placement = task_list
        task.save()

    return HttpResponse()


def update_task_list(request):
    task_list = get_object_or_404(TaskList, id=request.POST['task_list_id'])
    task_list.name = request.POST['name']

    if request.POST['toggle_archived'] == 'true':
        task_list.archived = not task_list.archived

    task_list.save()

    if (task_list.id == 1):
        template = 'scrum/backlog.html'
    else:
        template = 'scrum/sprint.html'

    return HttpResponse(render_task_list(task_list, template))


def delete_task_list(request):
    task_list = TaskList.objects.get(id=request.POST['task_list_id'])
    task_list.delete()
    return HttpResponse()


def empty_task_list(request):
    project = get_object_or_404(Project, id=request.POST['project_id'])

    task_list = TaskList(
        name='Sprint',
        created_at=timezone.now(),
        project=project,
        archived=False,
    )

    task_list.save()

    return HttpResponse(render_task_list(task_list, 'scrum/sprint.html'))


def index(request):
    project_id = 1
    project = get_object_or_404(Project, pk=project_id)
    task_lists = TaskList.objects.filter(project=project)

    tasks_lists_html = []

    for i in range(len(task_lists)):
        t = task_lists[i]
        if i < len(task_lists) - 1:
            tasks_lists_html.append(render_task_list(t, 'scrum/sprint.html'))
        else:
            tasks_lists_html.append(render_task_list(t, 'scrum/backlog.html'))

    project_html = project_selector(project_id)

    return render(request, 'scrum/index.html', {
        'project': project,
        'project_selector': project_html,
        'task_lists_html': tasks_lists_html,
    })
