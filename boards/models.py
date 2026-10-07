from django.db import models

# Create your models here.
class Board (models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    member_count = models.IntegerField()
    ticket_count = models.IntegerField()
    tasks_to_do_count = models.IntegerField()
    tasks_high_prio_count = models.IntegerField()
    owner_id = models.IntegerField()