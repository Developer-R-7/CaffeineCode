from django.db import models
from django.contrib.auth.models import User


class profile_register(models.Model):
    user = models.TextField(max_length=200,default="")
    github_username = models.TextField(max_length=40,default="")
    
    def __str__(self):
        return self.github_username
