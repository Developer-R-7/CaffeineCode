# Generated by Django 3.2.9 on 2021-11-14 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IndexHome', '0006_alter_profile_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='fail_otp_request',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='key',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='otp',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='resend_otp_request',
        ),
    ]