from django.shortcuts import render, redirect
from . import models, codes
from datetime import datetime, date
from django.contrib import messages
import bcrypt

def show_login_register(request):
    if 'user' in request.session:
        return redirect('/dashboard')
    return render(request, "login_register.html")

def show_dashboard(request):
    if 'user' not in request.session:
        return redirect('/')
    projects = models.get_projects()
    context = {
        'user': models.get_user(request.session['user']),
        'projects': models.get_projects()
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = models.User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="register")
        return redirect('/')
    users = models.filter_user_email(request.POST['email'])
    if len(users) > 0:
        messages.error(request, "this email is already found", extra_tags="register")
        return redirect('/')
    password = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()).decode()
    user = models.add_user(request.POST, password)
    
    request.session['user'] = user.id
    
    return redirect('/dashboard')

def login(request):
    if request.method == "GET":
        return redirect('/')
    errors = models.User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="login")
        return redirect('/')
    users = models.filter_user_email(request.POST['email'])
    if len(users) == 0:
        messages.error(request, "email or password not found", extra_tags="login")
        redirect('/')
    
    if not bcrypt.checkpw(request.POST['pass'].encode(), users[0].password.encode()):
        messages.error(request, "email or password not found", extra_tags="login")
    
    request.session['user'] = users[0].id
    
    return redirect('/dashboard')

def flush(request):
    codes.flush_session(request)
    return redirect('/')

def logout_from_dashboard(request):
    if request.method == "GET":
        return redirect('/dashboard')
    codes.flush_session(request)
    return redirect('/')

def show_create_project(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        "user" : models.get_user(request.session['user'])
    }
    return render(request, 'create_project.html', context)

def create_project(request):
    if request.method == "GET":
        return ('/createproject')
    errors = models.Project.objects.project_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="project")
        return redirect('/createproject')
    user_id = request.POST['user_id']
    project = models.add_project(request.POST, user_id)
    return redirect('/dashboard')

def logout_from_createproject(request):
    if request.method == "GET":
        return redirect('/createproject')
    codes.flush_session(request)
    return redirect('/')


def deleate_project(request):
    if request.method == "GET":
        return redirect('/dashboard')
    user = models.get_user(request.POST['user_id'])
    project = models.get_project(request.POST['project_id'])
    models.reomve_all_users_from_project(project)
    models.delete_project(project.id)
    return redirect('/dashboard')

def show_project_details(request, id):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        "enterd_user": models.get_user(request.session['user']),
        'project': models.get_project(id)
    }
    return render(request, 'project_details.html', context)

def logout_from_details(request, id):
    if request.method == "GET":
        return redirect(f'/project/{id}/details')
    codes.flush_session(request)
    return redirect('/')

def leave_from_project_inside_details(request, id):
    if request.method == "GRT":
        return redirect(f'/project/{id}/details')
    project = models.get_project(id)
    user = models.get_user(request.POST['user_id'])
    models.remove_user_from_project(project, user)
    return redirect(f'/project/{id}/details')


def show_edit(request, id):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'user': models.get_user(request.session['user']),
        'project' : models.get_project(id)
    }
    return  render(request, 'edit_project.html', context)

def edit_project(request, id):
    if request.method == "GET":
        return redirect(f'/editproject/{id}')
    errors = models.Project.objects.edit_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags="edit")
        return redirect(f'/editproject/{id}')
    
    models.update_project_title(id, request.POST['name'])
    models.update_project_desc(id, request.POST['desc'])
    models.update_project_sdate(id, request.POST['sdate'])
    models.update_project_endate(id, request.POST['endate'])
    return redirect("/dashboard")


def logout_from_edit(request, id):
    if request.method == "GET":
        return redirect(f"/editproject/{id}")
    codes.flush_session(request)
    return redirect('/')

def delete_from_details(request, id):
    if request.method == "GET":
        return redirect(f"/project/{id}/details")
    project = models.get_project(id)
    models.reomve_all_users_from_project(project)
    models.delete_project(id)
    return redirect('/dashboard')

def join_in_project(request):
    if request.method == "GET":
        return redirect('/dashboard')
    project = models.get_project(request.POST['project_id'])
    user = models.get_user(request.POST['user_id'])
    models.enter_to_project(project, user)
    return redirect('/dashboard')

def leave_in_project(request):
    if request.method == "GET":
        return redirect('/dashboard')
    project = models.get_project(request.POST['project_id'])
    user = models.get_user(request.POST['user_id'])
    models.remove_user_from_project(project, user)
    return redirect('/dashboard')