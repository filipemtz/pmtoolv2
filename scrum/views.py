from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.views import generic
from .models import Project, Task, TaskList, TaskListFeeling, TaskListType, TaskStatus, TaskWorkload
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.template import loader
from django.shortcuts import get_object_or_404, redirect, render
from typing import Dict, List
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import urllib
import io
import base64
from django.contrib.auth.decorators import login_required

matplotlib.use('Agg')
sns.set_style('whitegrid')
font = {
    'family': ['Tahoma', 'DejaVu Sans', 'Lucida Grande', 'Verdana'],
    'size': 14,
}
matplotlib.rc('font', **font)


class ProjectListView(generic.ListView):
    model = Project


class ProjectDetailView(generic.DetailView):
    model = Project


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


def render_selector(options: List[Dict], name: str, id, onselect_event: str = '', selector_class='') -> str:
    status_selector_html = loader.get_template('scrum/selector.html').render({
        "name": name,
        "id": id,
        "options": options,
        'onselect_event': onselect_event,
        'selector_class': selector_class,
    })
    return status_selector_html


def render_image_selector(options: List[Dict], name: str, id, onselect_event: str = '') -> str:
    status_selector_html = loader.get_template('scrum/img_selector.html').render({
        "name": name,
        "id": id,
        "options": options,
        'onselect_event': onselect_event,
    })
    return status_selector_html


def status_selector(selected_value: str = '', onselect_event: str = '') -> str:
    all_status = TaskStatus.choices

    selector_class = ''
    status_options = []

    for s in all_status:
        selected = selected_value == s[0]

        if selected:
            selector_class = "status_" + s[0]

        status_options.append({
            'name': s[1],
            'value': s[0],
            'selected': selected
        })

    selector_class += ' center roundbox'

    return render_selector(
        status_options,
        name='status',
        id='status',
        selector_class=selector_class,
        onselect_event=onselect_event
    )


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


def project_selector(user, selected_value: int = -1):
    user_projects = Project.objects.filter(team__id=user.id)

    options = [
        {
            'name': o.name,
            'value': o.id,
            'selected': selected_value == o.id
        }
        for o in user_projects
    ]

    options.append({
        'name': '+ new project',
        'value': 'new',
        'selected': False
    })

    onselect_event = "load_project_scrum($(this).val());"

    return render_selector(
        options, name='project', id='project', onselect_event=onselect_event)


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


def update_task(request):
    task = get_object_or_404(Task, id=request.POST['task_id'])
    task.name = request.POST['name']
    task.workload = request.POST['workload']

    if task.status != request.POST['status']:
        task.status = request.POST['status']
        task.status_update = timezone.now()

    if 'observation' in request.POST:
        task.observation = request.POST['observation']

    task.save()

    return HttpResponse(render_task(task))


def delete_task(request):
    task = Task.objects.get(id=request.POST['task_id'])
    task.delete()
    return HttpResponse()


def get_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)
    return HttpResponse(render_task(task))


def task_details_form(request):
    task = get_object_or_404(Task, id=request.POST['task_id'])
    onselect_event = f"save_task({task.id});"
    status_selector_html = status_selector(
        selected_value=task.status, onselect_event=onselect_event)
    workload_selector_html = workload_selector(
        selected_value=task.workload, onselect_event=onselect_event)
    return render(request, 'scrum/task-details.html', {
        'task': task,
        "workload_selector_html": workload_selector_html,
        "status_selector_html": status_selector_html,
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
    )

    task.save()

    return HttpResponse(render_task(task))


def render_task_list(task_list: TaskList, template: str) -> str:
    subtasks = Task.objects.filter(placement=task_list)
    subtasks_html = [render_task(t) for t in subtasks]
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

    return HttpResponse(render_task_list(task_list, 'scrum/sprint.html'))


def create_burndown_chart(request):
    task_list = get_object_or_404(TaskList, id=request.POST['task_list_id'])
    tasks = Task.objects.filter(placement=task_list)

    total_points = sum([TaskWorkload.as_int(t.workload) for t in tasks])
    tasks_done = tasks.filter(status=TaskStatus.DONE).order_by('status_update')
    points_done = sum([TaskWorkload.as_int(t.workload) for t in tasks_done])

    real_chart_x, real_chart_y = [], []
    real_chart_x.append(task_list.start_date)
    real_chart_y.append(total_points)
    decremental_points = total_points

    for t in tasks_done:
        decremental_points -= TaskWorkload.as_int(t.workload)
        real_chart_x.append(t.status_update)
        real_chart_y.append(decremental_points)

    real_chart_x.append(task_list.end_date)
    real_chart_y.append(total_points - points_done)

    desired_chart_x, desired_chart_y = [], []
    desired_chart_x.append(task_list.start_date)
    desired_chart_x.append(task_list.end_date)
    desired_chart_y.append(total_points)
    desired_chart_y.append(0)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(real_chart_x, real_chart_y, marker='o')
    ax.plot(desired_chart_x, desired_chart_y, '--', marker='o')
    ax.set_ylabel('Task Points')
    ax.set_xlabel('Date')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(['real', 'desired'])
    plt.tight_layout()

    # extracted from https://medium.com/@mdhv.kothari99/matplotlib-into-django-template-5def2e159997
    # extracted from https://spapas.github.io/2021/02/08/django-matplotlib/#:~:text=If%20instead%20of,graph%20directly%C2%A0there!
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300)
    buf_as_string = base64.b64encode(buf.getvalue()).decode()
    uri = urllib.parse.quote(buf_as_string)

    return render(request, 'scrum/burndown.html', {'data': uri})


@login_required
def index(request):
    create_sample_project = False

    if "project_id" not in request.GET:
        user_projects = Project.objects.filter(team__id=request.user.id)
        if user_projects.count() > 0:
            project_id = user_projects.first().id
        else:
            # user does not have projects
            create_sample_project = True
    elif (request.GET['project_id'] == 'new'):
        create_sample_project = True
    else:
        project_id = int(request.GET['project_id'])

    if create_sample_project:
        project = create_project(request.user)
        project_id = project.id

    project = get_object_or_404(Project, pk=project_id)
    task_lists = TaskList.objects.filter(project=project)

    tasks_lists_html = []

    for i in range(len(task_lists)):
        t = task_lists[i]
        if t.task_list_type == TaskListType.BACKLOG:
            tasks_lists_html.append(
                render_task_list(t, 'scrum/backlog.html'))
        else:
            tasks_lists_html.append(
                render_task_list(t, 'scrum/sprint.html'))

    project_select_html = project_selector(request.user, project_id)

    return render(request, 'scrum/index.html', {
        'project': project,
        'project_selector': project_select_html,
        'task_lists_html': tasks_lists_html,
    })


def test_view(request):
    return render(request, 'registration/test.html')


def signup_is_valid(request):
    error_msgs = []

    if ('firstname' not in request.POST) or (len(request.POST['firstname']) == 0):
        error_msgs.append("first name is required.")
    if ('lastname' not in request.POST) or (len(request.POST['lastname']) == 0):
        error_msgs.append("last name is required.")
    if ('username' not in request.POST) or (len(request.POST['username']) == 0):
        error_msgs.append("user name is required.")
    if ('email' not in request.POST) or (len(request.POST['email']) == 0):
        error_msgs.append("email is required.")
    if ('password' not in request.POST) or (len(request.POST['password']) == 0):
        error_msgs.append("password is required.")
    if ('password-check' not in request.POST) or (len(request.POST['password-check']) == 0):
        error_msgs.append("repeat password is required.")

    if User.objects.filter(username=request.POST['username']).count() > 0:
        error_msgs.append("username already taken.")

    if User.objects.filter(email=request.POST['email']).count() > 0:
        error_msgs.append("email already registred.")

    if request.POST['password'] != request.POST['password-check']:
        error_msgs.append("passwords do not match.")

    is_valid = len(error_msgs) == 0

    return is_valid, error_msgs


def signup_user(request):
    new_user = User.objects.create_user(
        request.POST['username'],
        request.POST['email'],
        request.POST['password'])
    new_user.first_name = request.POST['firstname']
    new_user.last_name = request.POST['lastname']
    new_user.save()


def signup_form(request):
    error_msgs = ''
    if request.method == "POST":
        is_valid, error_msgs = signup_is_valid(request)
        if is_valid:
            signup_user(request)
            user = authenticate(
                request,
                username=request.POST['username'],
                password=request.POST['password']
            )
            login(request, user)
            return redirect('/scrum/')

    return render(request, 'registration/signup.html', {
        'error_msgs': error_msgs
    })


def add_team_member(request):
    project = get_object_or_404(Project, id=request.POST['project_id'])
    new_team_member = get_object_or_404(
        User, username=request.POST['username'])
    project.team.add(new_team_member)
    project.save()

    return render(request, 'scrum/project_user.html', {
        'project': project,
        'team_member': new_team_member,
    })


def remove_team_member(request):
    project = get_object_or_404(Project, id=request.POST['project_id'])
    user = get_object_or_404(User, id=request.POST['user_id'])

    if project.team.count() > 1:
        project.team.remove(user)
        project.save()
        return HttpResponse("ok")
    else:
        return HttpResponseBadRequest("Team must have at least one user.")


def create_project(user, name='New Project'):
    project = Project(name=name)
    project.save()
    project.team.add(user)
    project.save()

    backlog = TaskList(
        name="Backlog",
        created_at=timezone.now(),
        project=project,
        archived=False,
        start_date=timezone.now(),
        end_date=timezone.now(),
        task_list_type=TaskListType.BACKLOG,
    )
    backlog.save()
    return project


def new_project(request):
    project = create_project(request.user)
    html = f"<li><button style='color:red; background-color: white; border: none' onclick='remove_project({{ project.id }});'><i class='bi bi-x-lg'></i></button><a href='{project.get_absolute_url()}'>{project.name}</a></li>"
    return HttpResponse(html)


def update_project(request):
    project = get_object_or_404(Project, id=request.POST['project_id'])
    project.name = request.POST['name']
    project.save()
    return HttpResponse('ok')


def remove_project(request):
    project = get_object_or_404(Project, id=request.POST['project_id'])
    project.delete()
    return HttpResponse('ok')


def project_details_form(request):
    project = get_object_or_404(Project, id=request.POST['project_id'])
    return render(request, 'scrum/project_details.html', {'project': project})


def speed_chart(request):
    project = get_object_or_404(Project, id=request.POST['project_id'])
    sprints = TaskList.objects.filter(
        project=project, task_list_type=TaskListType.SPRINT)

    sprint_dates = [s.end_date for s in sprints]
    team_speed = [s.n_points_completed() for s in sprints]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sprint_dates, team_speed, marker='o')
    ax.set_ylabel('Total Task Points')
    ax.set_xlabel('Sprint Date')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend(['Team'])
    plt.tight_layout()

    # extracted from https://medium.com/@mdhv.kothari99/matplotlib-into-django-template-5def2e159997
    # extracted from https://spapas.github.io/2021/02/08/django-matplotlib/#:~:text=If%20instead%20of,graph%20directly%C2%A0there!
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300)
    buf_as_string = base64.b64encode(buf.getvalue()).decode()
    uri = urllib.parse.quote(buf_as_string)

    return render(request, 'scrum/burndown.html', {'data': uri})
