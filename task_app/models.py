from django.conf import settings
from django.db import models
from boards_app.models import Board

# Create your models here.
class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_tasks", blank=True)
    reviewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="reviewed_tasks", blank=True)
    due_date = models.DateField(null=True)

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)