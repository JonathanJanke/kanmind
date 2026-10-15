from django.contrib.auth.models import AbstractUser
from django.db import models

from .manager import UserManager


class User(AbstractUser):
    username = None
    fullname = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname"]

    def __str__(self):
        """Gibt den vollständigen Namen für lesbare Benutzer-Darstellungen zurück."""
        return self.fullname