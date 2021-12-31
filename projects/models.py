from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class profile_register(models.Model):
    user = models.TextField(max_length=200)
    github_username = models.TextField(max_length=40,default="")
    
    def __str__(self):
        return self.github_username
