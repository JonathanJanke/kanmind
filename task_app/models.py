from django.db import models
from boards_app.models import Board

# Create your models here.
class Task(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    assignee_id = models.IntegerField(null=True, blank=True)
    reviewer_id = models.IntegerField(null=True, blank=True)
    due_date = models.DateField(null=True)
