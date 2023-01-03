
import random
from typing import List, Optional, Tuple

from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.template import loader

from scrum.models import UserNote

from scrum.views.project import project_selector
from scrum.views.components import render_selector, render_image_selector


@login_required
def user_note(request):
    notes = UserNote.objects.filter(user=request.user)

    if notes.count() == 0:
        # create a new note
        note = UserNote(user=request.user, title='New Note')
        note.save()
    else:
        note = notes.first()

    return render(request, 'scrum/user_note.html', {"note": note})


@login_required
def update_user_note(request, pk):
    if (request.method != 'POST') or ('content' not in request.POST):
        return HttpResponseBadRequest()

    note = get_object_or_404(UserNote, pk=pk)
    note.content = request.POST['content']
    note.save()

    return HttpResponse(note.content)
