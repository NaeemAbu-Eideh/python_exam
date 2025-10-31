from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('input-date', views.input_date),
]