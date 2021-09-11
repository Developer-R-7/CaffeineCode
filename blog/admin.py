from django.contrib import admin

# Register your models here.
from .models import Category, Post
admin.site.register(Post)
admin.site.register(Category)