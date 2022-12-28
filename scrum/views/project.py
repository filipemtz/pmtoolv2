
from django.utils import timezone
from django.views import generic
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,  render

from scrum.models import Project, TaskList, TaskListType
from scrum.views.components import render_selector


class ProjectListView(generic.ListView):
    model = Project


class ProjectDetailView(generic.DetailView):
    model = Project


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

    routine = TaskList(
        name="Routine",
        created_at=timezone.now(),
        project=project,
        archived=False,
        start_date=timezone.now(),
        end_date=timezone.now(),
        task_list_type=TaskListType.ROUTINE,
    )

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
    routine.save()

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
    return HttpResponse('ok')  # is there a better way of doing this?


def project_details_form(request):
    project = get_object_or_404(Project, id=request.POST['project_id'])
    return render(request, 'scrum/project_details.html', {'project': project})


def project_notes_editor(request, pk):
    project = get_object_or_404(Project, id=pk)

    if request.method == 'GET':
        return render(request, 'scrum/project_notes_editor.html', {'project': project})
    elif request.method == 'POST':
        if 'notes' in request.POST:
            project.notes = request.POST['notes']
            project.save()
            return HttpResponse(project.notes)

    return HttpResponseBadRequest()
