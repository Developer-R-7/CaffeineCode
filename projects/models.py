from django.db import models

# Create your models here.

class profile_register(models.Model):
    username = models.TextField()
    
    def __str__(self):
        return self.username
