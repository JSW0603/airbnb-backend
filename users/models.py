from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    name = models.CharField(max_length=140, default="")
    is_host = models.BooleanField(default=False)
