from django.urls import include, path

from . import views

urlpatterns = [
    # index
    path('', views.index, name='index'),
    # users
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup', views.signup_form, name="signup"),
    path('edit/<int:pk>', views.UserUpdateView.as_view(), name="edit-profile"),
    # projects
    path('projects', views.ProjectListView.as_view(), name="projects"),
    path('project/<int:pk>', views.ProjectDetailView.as_view(), name="project"),
    path('project/add_team_member',
         views.add_team_member, name="add_team_member"),
    path('project/remove_team_member',
         views.remove_team_member, name="remove_team_member"),
    path('project/new', views.new_project, name="new_project"),
    path('project/update', views.update_project, name="update_project"),
    path('project/remove', views.remove_project, name="remove_project"),
    path('project_details_form', views.project_details_form,
         name='project_details_form'),
    path('project/<int:pk>/archive',
         views.project_archived_sprints, name="project-archive"),
    path('project/<int:pk>/notes',
         views.project_notes_editor, name="project-notes-editor"),
    # tasks
    path('new_empty_task', views.create_empty_task, name='new_empty_task'),
    path('task/<int:task_id>', views.get_task, name='task'),
    path('update_task', views.update_task, name='update_task'),
    path('task_details_form', views.task_details_form, name='task_details_form'),
    path('update_priorities', views.update_priorities, name='update_priorities'),
    path('delete_task', views.delete_task, name='delete_task'),
    # task lists
    path('update_task_list', views.update_task_list, name='update_task_list'),
    path('delete_task_list', views.delete_task_list, name='delete_task_list'),
    path('empty_task_list', views.empty_task_list, name='empty_task_list'),
    path('task_list_details_form', views.task_list_details_form,
         name='task_list_details_form'),
    path('myactivities', views.my_activities, name="myactivities"),
    # charts
    path('burndown', views.create_burndown_chart, name='create_burndown_chart'),
    path('speed_chart', views.speed_chart, name="speed_chart"),
]
