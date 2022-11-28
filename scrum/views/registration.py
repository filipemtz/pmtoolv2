

from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect, render


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
