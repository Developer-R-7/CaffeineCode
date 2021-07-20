from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_verfied = models.BooleanField(default=False)
    account_id = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField(default="abc@mail.com")

    def __str__(self):
        return self.user.username