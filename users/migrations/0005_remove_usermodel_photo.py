# Generated by Django 5.1.3 on 2024-11-30 20:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_usermodel_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermodel',
            name='photo',
        ),
    ]