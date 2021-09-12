from celery import shared_task
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from time import sleep
from celery.decorators import task




@task()
def SendOTP(email,otp):
    #send_mail('HELLO TEST MAIL','THIS MAIL IS SENT BY CELERY',settings.EMAIL_HOST_USER,[email],fail_silently=True)
    html_content = render_to_string("IndexHome/email.html",{'otp':otp,'email':email})
    text_content = strip_tags(html_content)
    email_con = EmailMultiAlternatives('Verfication Code - CaffeineCode',text_content,settings.EMAIL_HOST_USER,[email]) 
    email_con.attach_alternative(html_content,"text/html")
    email_con.send()
    return "Done"
