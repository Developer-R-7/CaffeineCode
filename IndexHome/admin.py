from django.contrib import admin

# Register your models here.
from .models import Contact, Newsletter, Profile
admin.site.register(Profile)
admin.site.register(Newsletter)
admin.site.register(Contact)
