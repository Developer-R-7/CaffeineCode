# Generated by Django 3.2.9 on 2021-11-19 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IndexHome', '0010_profile_fail_attepmt'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='resend_request',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='key',
            field=models.TextField(default='empty', max_length=200),
        ),
    ]
