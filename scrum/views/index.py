
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from scrum.models import (Project, TaskList,
                          TaskListType, UserGuiPreferences)

from scrum.views.project import create_project, project_selector
from scrum.views.task_list import render_task_list


@login_required
def index(request):
    create_sample_project = False

    preferences, _ = UserGuiPreferences.objects.get_or_create(
        user=request.user)

    project_id = -1

    if "project_id" not in request.GET:
        if preferences.selected_project is not None:
            project = preferences.selected_project
            project_id = project.id
        else:
            user_projects = Project.objects.filter(team__id=request.user.id)
            if user_projects.count() > 0:
                project = user_projects.first()
                project_id = project.id
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
    preferences.selected_project = project
    preferences.save()

    tasks_lists_html = []

    sprints = TaskList.objects.filter(
        project=project, task_list_type=TaskListType.SPRINT)

    if len(sprints) > 0:
        tasks_lists_html.append(render_task_list(
            sprints[0], 'scrum/sprint.html'))

    backlog = TaskList.objects.filter(
        project=project, task_list_type=TaskListType.BACKLOG).first()

    tasks_lists_html.append(render_task_list(backlog, 'scrum/backlog.html'))

    routine = TaskList.objects.filter(
        project=project, task_list_type=TaskListType.ROUTINE).first()

    if routine is not None:
        tasks_lists_html.append(render_task_list(
            routine, 'scrum/routine.html'))

    for i in range(1, len(sprints)):
        t = sprints[i]
        tasks_lists_html.append(
            render_task_list(t, 'scrum/sprint.html'))

    project_select_html = project_selector(request.user, project_id)

    return render(request, 'scrum/index.html', {
        'project': project,
        'project_selector': project_select_html,
        'task_lists_html': tasks_lists_html,
    })
