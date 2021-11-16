from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_verfied = models.BooleanField(default=False)
    account_id = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField()
    subscribe_newsletter = models.BooleanField(default=False)
    key = models.BinaryField(default=b'')
    otp = models.TextField(max_length=6,default="xxxxxx")


    def __str__(self):
        return self.user.username

