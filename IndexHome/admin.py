from django.contrib import admin

# Register your models here.
from .models import Newsletter, Profile
admin.site.register(Profile)
admin.site.register(Newsletter)
