# Generated by Django 2.2.16 on 2022-03-06 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='confirmation_code',
        ),
    ]
