

from django.urls import path
from task_app.views import ReviewingToUserView, TaskListView, AssignedToUserView

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/assigned-to-me/", AssignedToUserView.as_view(), name="assigned-to-me"),
    path("tasks/reviewing/", ReviewingToUserView.as_view(), name="reviewing-to-me"),
]