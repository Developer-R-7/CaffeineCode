from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_verfied = models.BooleanField(default=False)
    account_id = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField()
    key = models.TextField(default="empty", max_length=200)
    otp = models.TextField(max_length=6, default="xxxxxx")
    fail_attepmt = models.SmallIntegerField(default=0)
    resend_request = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.user.username

class Newsletter(models.Model):
    subscribe_mail = models.EmailField()

    def __str__(self):
        return self.subscribe_mail

class Notify(models.Model):
    notify_mail = models.EmailField()

    def __str__(self):
        return self.notify_mail

class Contact(models.Model):
    name = models.TextField(max_length=100)
    subject = models.TextField(max_length=100)
    body = models.TextField(max_length=600)
    email = models.EmailField()

    def __str__(self):
        return "Query |" + str(self.pk)