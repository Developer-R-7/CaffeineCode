from django.contrib import admin
from .models import Contact, Newsletter, Profile

admin.site.register(Profile)
admin.site.register(Newsletter)
admin.site.register(Contact)
