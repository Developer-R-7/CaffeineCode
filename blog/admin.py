from django.contrib import admin

# Register your models here.
from .models import Post,Newsletter
admin.site.register(Post)
admin.site.register(Newsletter)