from django.db import models
from django.contrib.auth.models import AbstractUser

from LabrinFSH.utils.base import BaseModel


class User(AbstractUser):
    email = models.EmailField(unique=True, default="")
    username = models.CharField(max_length=255, verbose_name="Username", default="")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
