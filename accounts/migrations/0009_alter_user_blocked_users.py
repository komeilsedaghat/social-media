# Generated by Django 4.0 on 2022-05-15 19:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_bloked_users_user_blocked_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blocked_users',
            field=models.ManyToManyField(related_name='blocked', to=settings.AUTH_USER_MODEL),
        ),
    ]
