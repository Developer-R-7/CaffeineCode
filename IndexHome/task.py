from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from time import sleep
from celery.decorators import task




@task()
def SendOTP(email,otp):
    send_mail('HELLO TEST MAIL','THIS MAIL IS SENT BY CELERY',settings.EMAIL_HOST_USER,[email],fail_silently=True)
    return "Done"
