# Generated by Django 3.2.5 on 2021-07-26 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20210725_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='designation',
            field=models.CharField(default='freelancer', max_length=60),
        ),
        migrations.AddField(
            model_name='post',
            name='skills',
            field=models.CharField(default='html,css', max_length=70),
        ),
    ]
