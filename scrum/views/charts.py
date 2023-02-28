
from datetime import date
import io
import base64
import urllib
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from scrum.models import (Project, Task, TaskList,
                          TaskListType, TaskStatus, TaskWorkload)

matplotlib.use('Agg')
sns.set_style('whitegrid')
font = {
    'family': ['Tahoma', 'DejaVu Sans', 'Lucida Grande', 'Verdana'],
    'size': 14,
}
matplotlib.rc('font', **font)


def create_burndown_chart(request):
    task_list = get_object_or_404(TaskList, id=request.POST['task_list_id'])
    tasks = Task.objects.filter(placement=task_list)

    if tasks.count() == 0:
        return HttpResponse("The sprint does not contain tasks yet.")

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
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
        tick.set_ha("center")
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


def count_points_per_month(concluded_tasks):
    # sort by time of conclusion
    concluded_tasks = sorted(concluded_tasks, key=lambda x: x.status_update)

    first_month = concluded_tasks[0].status_update.month
    first_year = concluded_tasks[0].status_update.year

    last_month = concluded_tasks[-1].status_update.month
    last_year = concluded_tasks[-1].status_update.year

    month, year = first_month, first_year
    dates = []
    sum_points = []
    task_idx = 0

    # walk month by month counting the points in each
    while (month != last_month) or (year != last_year):
        date_value = date(year, month, 1)
        points = 0

        while (concluded_tasks[task_idx].status_update.month == month) and \
                (concluded_tasks[task_idx].status_update.year == year):
            points += TaskWorkload.as_int(concluded_tasks[task_idx].workload)
            task_idx += 1

        sum_points.append(points)
        dates.append(date_value)

        month = month + 1
        if month > 12:
            month = 1
            year += 1

    return dates, sum_points


def speed_chart(request):
    project = get_object_or_404(Project, id=request.POST['project_id'])
    sprints = TaskList.objects.filter(
        project=project, task_list_type=TaskListType.SPRINT)

    if sprints.count() == 0:
        return HttpResponse("The project does not contain sprints yet.")

    sprint_dates = []
    team_speed = []

    for s in sprints:
        points = s.total_points()
        sprint_dates.append(s.start_date)
        team_speed.append(points)
        sprint_dates.append(s.end_date)
        team_speed.append(points)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(sprint_dates, team_speed, marker='o')

    ax.set_ylabel('Total Task Points')
    ax.set_xlabel('Sprint Date')
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
        tick.set_ha("center")

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


def personal_speed_chart(request):
    # users tasks that were concluded
    concluded_tasks = list(Task.objects.filter(
        responsible_id=request.user.id,
        status=TaskStatus.DONE).all())

    dates, sum_points = count_points_per_month(concluded_tasks)

    if (len(dates) == 0) or (len(sum_points) == 0):
        return HttpResponse("User has not finished any task so far.")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(dates, sum_points, marker='o')

    ax.set_ylabel('Total Task Points')
    ax.set_xlabel('Month')
    for tick in ax.get_xticklabels():
        tick.set_rotation(30)
        tick.set_ha("center")

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend([request.user.first_name])
    plt.tight_layout()

    # extracted from https://medium.com/@mdhv.kothari99/matplotlib-into-django-template-5def2e159997
    # extracted from https://spapas.github.io/2021/02/08/django-matplotlib/#:~:text=If%20instead%20of,graph%20directly%C2%A0there!
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300)
    buf_as_string = base64.b64encode(buf.getvalue()).decode()
    uri = urllib.parse.quote(buf_as_string)

    return render(request, 'scrum/burndown.html', {'data': uri})
