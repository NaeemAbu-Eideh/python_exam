from django.db import models
import re
from datetime import datetime, date

class UserManager(models.Manager):
    def register_validator(self, request):
        errors = {}
        emails_pattern = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        
        if('fname' in request and request['fname'] == ''):
            errors['fname'] = "please fill the First Name"
        
        elif('fname' in request and len(request['fname']) < 2):
            errors['fname'] = "First Name shuld have at least 2 chars"
        
        if('lname' in request and request['lname'] == ''):
            errors['lname'] = "please fill the Last Name"
            
        elif('lname' in request and len(request['lname']) < 2):
            errors['lname'] = "Last Name shuld have at least 2 chars"
            
        if('email' in request and request['email'] == ''):
            errors['email'] = "please fill the email"
        
        elif('email' in request and not emails_pattern.match(request['email'])):
            errors['email'] = "email does not match"
        
        if ('pass' in request and request['pass'] == ''):
            errors['pass'] = "please fill the Password"
        
        elif ('pass' in request and len(request['pass']) < 8):
            errors['pass'] = "password shod have at least 8 characters"
        
        if ('cpass' in request and request['cpass'] == ''):
            errors['cpass'] = "please fill the Confirm Password"
        
        if ('cpass' in request and 'pass' in request and request['pass'] != request['cpass']):
            errors['match'] = "confirm password must be equal password"
        return errors
    
    def login_validator(self, request):
        errors = {}
        emails_pattern = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if('email' in request and request['email'] == ''):
            errors['email'] = "please fill the email"
        
        elif('email' in request and not emails_pattern.match(request['email'])):
            errors['email'] = "email does not match"
        
        if ('pass' in request and request['pass'] == ''):
            errors['pass'] = "please fill the Password"
        return errors

class ProjectManager(models.Manager):
    def project_validator(self, request):
        errors = {}
        sdate = request['sdate']
        endate = request['endate']
        
        if request['name'] == "":
            errors['name'] = "Name should not be empty"
        elif len(request['name']) < 2:
            errors['name'] = "Name should be at least 2 chars"
        
        if request['desc'] == "":
            errors['desc'] = "Description should not be empty"
        
        elif len(request['desc']) < 10:
            errors['desc'] = "Description should be at least 10 chars"
        
        if request['sdate'] == "":
            errors["sdate"] = "Start date should not be blank"
        
        else:
            start_date = datetime.strptime(sdate, "%Y-%m-%d").date()
            if start_date < date.today() or start_date > date.today():
                errors['sdate'] = "Start Date should be in present"
        
        if request['endate'] == "":
            
            errors["endate"] = "End date should not be blank"
        
        else:
            end_date = datetime.strptime(endate, "%Y-%m-%d").date()
            if end_date < date.today():
                errors['endate'] = "End Date should be in present"
        return errors
    def edit_validator(self, request):
        errors = {}
        sdate = request['sdate']
        endate = request['endate']
        
        if request['name'] == "":
            errors['name'] = "Name should not be empty"
        elif len(request['name']) < 2:
            errors['name'] = "Name should be at least 2 chars"
        
        if request['desc'] == "":
            errors['desc'] = "Description should not be empty"
        
        elif len(request['desc']) < 10:
            errors['desc'] = "Description should be at least 10 chars"
        
        if request['sdate'] == "":
            errors["sdate"] = "Start date should not be blank"
        
        else:
            start_date = datetime.strptime(sdate, "%Y-%m-%d").date()
            if (start_date > date.today()):
                errors['sdate'] = "Start Date should be in present"
            elif start_date != date.today():
                if start_date != request['old_start_date']:
                    errors['sdate'] = "Start Date should be in present"
        if request['endate'] == "":
            
            errors["endate"] = "End date should not be blank"
        
        else:
            end_date = datetime.strptime(endate, "%Y-%m-%d").date()
            if end_date < date.today():
                errors['endate'] = "End Date should be in present"
        return errors


class User(models.Model):
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Project(models.Model):
    title = models.CharField(max_length=30)
    desc = models.TextField()
    sdate = models.DateField()
    endate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="project_creation", on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name="projects")
    objects = ProjectManager()


def add_user(post, password):
    return User.objects.create(fname = post['fname'], lname = post['lname'], email = post['email'], password = password)

def filter_user_email(email):
    return User.objects.filter(email = email)

def get_projects():
    return Project.objects.all()

def get_user(id):
    return User.objects.get(id = id)

def add_project(post, user_id):
    user = get_user(user_id)
    project = Project.objects.create(title = post['name'], desc = post['desc'], sdate = post['sdate'], endate = post['endate'], creator = user)
    project.users.add(user)
    return project

def get_project(id):
    return Project.objects.get(id = id)

def remove_user_from_project(project, user):
    project.users.remove(user)

def reomve_all_users_from_project(project):
    project.users.clear()

def delete_project(id):
    project = Project.objects.get(id = id)
    project.delete()

def update_project_title(id, title):
    project = get_project(id)
    Project.title = title
    project.save()

def update_project_desc(id, desc):
    project = get_project(id)
    Project.desc = desc
    project.save()

def update_project_sdate(id, sdate):
    project = get_project(id)
    Project.sdate = sdate
    project.save()

def update_project_endate(id, endate):
    project = get_project(id)
    Project.endate = endate
    project.save()

def enter_to_project(project, user):
    project.users.add(user)
