from django.urls import path
from task_app.views import TaskListView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
]