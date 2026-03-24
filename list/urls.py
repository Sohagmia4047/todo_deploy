from django.urls import path
from . import views

urlpatterns = [
    path('', views.todo_view, name='home'),
    path('todo/', views.todo_view, name='todo_view'),
    path('done/<int:task_id>/', views.done_view, name='done_view'),
    path('delete/<int:task_id>/', views.delete_view, name='delete_view'),
]