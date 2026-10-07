from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    fullname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname"]

    def __str__(self):
        return self.fullname