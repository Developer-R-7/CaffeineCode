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

    def __str__(self):
        return self.user.username

class Code(models.Model):
    author = models.ForeignKey(Profile,on_delete=models.CASCADE)
    date_uploded = models.DateTimeField()
    code_title = models.CharField(max_length=100)
    language_tags = TaggableManager()


    def __str__(self):
        return self.code_title
