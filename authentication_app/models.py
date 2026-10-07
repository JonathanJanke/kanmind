from django.db import models

# Create your models here.
class User(models.Model):
    fullname = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    repeat_password = models.CharField(max_length=128)

    def __str__(self):
        return self.fullname