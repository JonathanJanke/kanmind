

from django.urls import path
from task_app.api.views import ReviewingToUserView, TaskListView,SingleTaskView, AssignedToUserView,CommentListView

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:task_id>/", SingleTaskView.as_view(), name="single-task"),
    path("tasks/<int:task_id>/comments/", CommentListView.as_view(), name="task-comments"),
    path("tasks/<int:task_id>/comments/<int:comment_id>/", CommentListView.as_view(), name="single-comment"),
    path("tasks/assigned-to-me/", AssignedToUserView.as_view(), name="assigned-to-me"),
    path("tasks/reviewing/", ReviewingToUserView.as_view(), name="reviewing-to-me"),
]