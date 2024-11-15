# Generated by Django 5.1.3 on 2024-11-13 00:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userconfirmmodel_is_confirmed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='auth_status',
            field=models.CharField(choices=[('NEW', 'new'), ('CODE_VERIFIED', 'code_verified'), ('DONE', 'done'), ('PHOTO_STEP', 'photo_step')], default='NEW', max_length=50),
        ),
        migrations.CreateModel(
            name='FollowingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Follower',
                'verbose_name_plural': 'Followers',
                'unique_together': {('user', 'to_user')},
            },
        ),
    ]
