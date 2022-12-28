
import random
from typing import List, Optional, Tuple

from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.template import loader

from scrum.models import (Project, Task, TaskList, TaskListFeeling,
                          TaskListType, TaskStatus, TaskWorkload, Tag, TaskTag)

from scrum.views.project import project_selector
from scrum.views.components import render_selector, render_image_selector

task_templates = {
    TaskListType.BACKLOG: "task.html",
    TaskListType.SPRINT: "task.html",
    TaskListType.ROUTINE: "routine_task.html",
}


def status_selector(task: Task) -> str:
    icon = TaskStatus.as_icon(task.status)

    return loader.get_template('scrum/task_status_selector.html').render({
        'task': task,
        'status_icon': icon
    })


def team_member_selector(team: List[User], selected_value: User, onselect_event: str = '') -> str:
    responsible_id = -1
    if selected_value is not None:
        responsible_id = selected_value.id

    options = [
        {
            'name': user.username,
            'value': user.id,
            'selected': responsible_id == user.id
        }
        for user in team
    ]

    return render_selector(
        options, name='responsible', id='responsible', onselect_event=onselect_event)


def feeling_selector(selected_value: str = '', onselect_event: str = '') -> str:
    all_status = TaskListFeeling.choices

    if selected_value == '':
        selected_value = 'UN'

    status_options = [
        {
            'name': TaskListFeeling.as_emoji(s),
            'value': s[0],
            'description': s[1].capitalize(),
            'selected': selected_value == s[0],
        }
        for s in all_status
    ]

    return render_image_selector(
        status_options,
        name='feeling',
        id='feeling',
        onselect_event=onselect_event
    )


def workload_selector(selected_value: str = '', onselect_event: str = ''):
    all_objs = TaskWorkload.choices

    options = [
        {
            'name': o[1],
            'value': o[0],
            'selected': selected_value == o[0]
        }
        for o in all_objs
    ]

    return render_selector(
        options, name='workload', id='workload', onselect_event=onselect_event)


def random_rgb_color() -> Tuple[int, int, int]:
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    return (red, green, blue)


def text_color_from_bg_color(
        color: Tuple[int, int, int]) -> Tuple[int, int, int]:

    # If background color is bright, text_color will be black. Otherwise,
    # it will be white.
    avg_color = (color[0] + color[1] + color[2]) // 3

    # the threshold was manually calibrated based on qualitative analysis
    # of the colors
    if avg_color > 160:
        text_color = (0, 0, 0)
    else:
        text_color = (255, 255, 255)

    return text_color


def color_to_rgb_string(color: Tuple[int, int, int]) -> str:
    return '#%02x%02x%02x' % color


def register_tags(tags_from_string: List[str], task: Task):
    project = task.placement.project
    tags_in_project = list(Tag.objects.filter(project=project).all())

    for tag in tags_from_string:
        tag_found = False
        for existing_tag in tags_in_project:
            if tag == existing_tag.name:
                TaskTag(task=task, tag=existing_tag).save()
                tag_found = True
                break

        if not tag_found:
            color = random_rgb_color()
            text_color = text_color_from_bg_color(color)

            new_tag = Tag(name=tag,
                          color=color_to_rgb_string(color),
                          text_color=color_to_rgb_string(text_color),
                          project=project)

            new_tag.save()

            TaskTag(task=task, tag=new_tag).save()


def update_task(request):
    task = get_object_or_404(Task, id=request.POST['task_id'])

    tags, text_without_tags = Tag.extract_tags(request.POST['name'])

    task.name = text_without_tags
    task.workload = request.POST['workload']
    task.responsible = User.objects.get(id=request.POST['responsible'])

    if 'observation' in request.POST:
        task.observation = request.POST['observation']

    task.save()

    register_tags(tags, task)

    return HttpResponse(render_task(task))


def delete_task_tag(request, task_id, tag_id):
    task_tags = TaskTag.objects.filter(task_id=task_id, tag_id=tag_id)

    if task_tags.count() > 0:
        task_tag = task_tags.first()
        task_tag.delete()

        # remove the tag if it is not referenced in any other task
        if TaskTag.objects.filter(tag_id=tag_id).count() == 0:
            tags = Tag.objects.filter(id=tag_id)
            if tags.count() > 0:
                tags.first().delete()

    return HttpResponse()


def delete_task(request):
    task = Task.objects.get(id=request.POST['task_id'])
    task.delete()
    return HttpResponse()


def get_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    return HttpResponse(render_task(task))


def task_toggle_status(request, pk):
    task = get_object_or_404(Task, id=pk)

    if task.status == TaskStatus.TODO.value:
        task.status = TaskStatus.DONE
    else:
        task.status = TaskStatus.TODO

    task.status_update = timezone.now()
    task.save()

    return HttpResponse(TaskStatus.as_icon(task.status))


def task_details_form(request):
    task = get_object_or_404(Task, id=request.POST['task_id'])
    onselect_event = f"save_task({task.id});"

    status_selector_html = status_selector(task=task)

    workload_selector_html = workload_selector(
        selected_value=task.workload, onselect_event=onselect_event)

    team = task.placement.project.team.all()

    team_member_selector_html = team_member_selector(
        team, selected_value=task.responsible, onselect_event=onselect_event)

    return render(request, 'scrum/task-details.html', {
        'task': task,
        "workload_selector_html": workload_selector_html,
        "status_selector_html": status_selector_html,
        "team_member_selector_html": team_member_selector_html,
    })


def task_list_details_form(request):
    task_list = get_object_or_404(TaskList, id=request.POST['task_list_id'])

    feeling = feeling_selector(
        task_list.feeling,
        onselect_event=f"update_task_list({task_list.id}, false);"
    )

    return render(request, 'scrum/sprint_details.html', {
        'task_list': task_list,
        'feeling_selector': feeling,
    })


def create_empty_task(request):
    task_list = get_object_or_404(TaskList, id=request.POST['task_list_id'])
    bottom_or_top_priority = request.POST['bottom_or_top']

    priority = 1
    if bottom_or_top_priority == 'bottom':
        low_priority_task = Task.lowest_priority_task()
        if low_priority_task:
            priority = low_priority_task.priority + 1
    else:
        for t in Task.objects.filter(placement=task_list):
            t.priority += 1
            t.save()

    task = Task(
        name='new task',
        priority=priority,
        workload=TaskWorkload.SMALL_1,
        status=TaskStatus.TODO,
        placement=task_list,
        status_update=timezone.now(),
        responsible=request.user
    )

    task.save()

    return HttpResponse(render_task(task))


def render_task_list(task_list: TaskList, template: str) -> str:
    subtasks = Task.objects.filter(placement=task_list)
    team = task_list.project.team.all()
    subtasks_html = [render_task(t, team) for t in subtasks]
    feeling = feeling_selector(
        task_list.feeling,
        onselect_event=f"update_task_list({task_list.id}, false);"
    )
    task_list_html = loader.get_template(template).render({
        "task_list": task_list,
        "subtasks": subtasks_html,
        "feeling_selector": feeling,
    })
    return task_list_html


def render_task(task: Task, team: Optional[List[User]] = None) -> str:
    onselect_event = f"save_task({task.id});"

    status_selector_html = status_selector(task)

    workload_selector_html = workload_selector(
        selected_value=task.workload, onselect_event=onselect_event)

    task_template = task_templates[task.placement.task_list_type]

    if team is None:
        # highly inefficient
        team = task.placement.project.team.all()

    team_member_selector_html = team_member_selector(
        team,
        selected_value=task.responsible,
        onselect_event=onselect_event
    )

    tags = TaskTag.objects.filter(task=task).all()
    tags = [t.tag for t in tags]

    task_html = loader.get_template(f'scrum/{task_template}').render({
        "task": task,
        "workload_selector_html": workload_selector_html,
        "status_selector_html": status_selector_html,
        "team_member_selector_html": team_member_selector_html,
        "tags": tags
    })

    return task_html


def extract_int_id(html_id):
    return int(html_id.split("_")[-1])


def update_priorities(request):
    if 'task_list_id' not in request.POST:
        return HttpResponseNotFound()

    task_list_id = request.POST['task_list_id']

    if len(task_list_id) > 0:
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
    task_list.start_date = datetime.strptime(
        request.POST['start_date'], '%Y-%m-%d')
    task_list.end_date = datetime.strptime(
        request.POST['end_date'], '%Y-%m-%d')

    if request.POST['toggle_archived'] == 'true':
        task_list.archived = not task_list.archived

    if 'observation' in request.POST:
        task_list.observation = request.POST['observation']

    if 'feeling' in request.POST:
        task_list.feeling = request.POST['feeling']

    task_list.save()

    if (task_list.task_list_type == TaskListType.BACKLOG):
        template = 'scrum/backlog.html'
    elif (task_list.task_list_type == TaskListType.BACKLOG):
        template = 'scrum/routine.html'
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
        start_date=timezone.now(),
        end_date=timezone.now(),
    )

    task_list.save()

    # ####################################
    # add routine tasks into the sprint
    # ####################################
    routine = TaskList.objects.filter(
        project=project, task_list_type=TaskListType.ROUTINE).first()

    if routine is not None:
        routine_tasks = Task.objects.filter(placement=routine)
        for counter, task in enumerate(routine_tasks):
            task = Task(
                name=task.name,
                priority=(counter + 1),
                workload=task.workload,
                status=TaskStatus.TODO,
                placement=task_list,
                status_update=timezone.now(),
                responsible=request.user
            )

            task.save()

    return HttpResponse(render_task_list(task_list, 'scrum/sprint.html'))


@login_required
def my_activities(request):
    user_tasks = Task.objects.filter(
        responsible=request.user,
        placement__task_list_type=TaskListType.SPRINT,
        placement__end_date__gte=timezone.now()
    )

    total = 0
    done = 0
    todo = 0
    in_progress = 0

    for t in user_tasks:
        points = TaskWorkload.as_int(t.workload)
        total += points
        if t.status == TaskStatus.DONE:
            done += points
        elif t.status == TaskStatus.IN_PROGRESS:
            in_progress += points
        else:
            todo += points

    return render(request, 'scrum/my_activities.html', {
        "subtasks": [render_task(t) for t in user_tasks],
        "total_points": total,
        "todo": todo,
        "in_progress": in_progress,
        "done": done,
    })


def project_archived_sprints(request, pk):
    project = get_object_or_404(Project, pk=pk)

    tasks_lists_html = []

    sprints = TaskList.objects.filter(
        project=project,
        task_list_type=TaskListType.SPRINT,
        archived=True
    )

    for i in range(1, len(sprints)):
        t = sprints[i]
        tasks_lists_html.append(
            render_task_list(t, 'scrum/sprint.html'))

    project_select_html = project_selector(request.user, pk)

    return render(request, 'scrum/index.html', {
        'project': project,
        'project_selector': project_select_html,
        'task_lists_html': tasks_lists_html,
        'active_page': 'archive'
    })
