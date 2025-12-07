# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name="task_list"),  # NOTE: task_list, pas index
    path('create/', views.create_task, name="create_task"),
    path('update/<int:pk>/', views.update_task, name="update_task"),  # NOTE: update_task, pas updateTask
    path('delete/<int:pk>/', views.delete_task, name="delete_task"),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('toggle/<int:pk>/', views.toggle_complete, name='toggle_complete'),
    path('filter/<str:priority>/', views.filter_by_priority, name='filter_priority'),
]
