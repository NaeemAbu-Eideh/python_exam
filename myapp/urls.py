from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_login_register),
    path('register', views.register),
    path('dashboard/', views.show_dashboard),
    path('login', views.login),
    path('flush', views.flush),
    path('dashboard/logout', views.logout_from_dashboard),
    path('createproject/', views.show_create_project),
    path('createproject/create', views.create_project),
    path('createproject/logout', views.logout_from_createproject),
    path('dashboard/deleate', views.deleate_project), 
    path('project/<int:id>/details/', views.show_project_details),
    path('project/<int:id>/details/logout', views.logout_from_details),
    path('project/<int:id>/details/separate', views.leave_from_project_inside_details),
    path('editproject/<int:id>/', views.show_edit),
    path('editproject/<int:id>/edit', views.edit_project),
    path('editproject/<int:id>/logout', views.logout_from_edit),
    path('project/<int:id>/details/delete', views.delete_from_details),
    path('dashboard/Join', views.join_in_project),
    path('dashboard/separate', views.leave_in_project)
]