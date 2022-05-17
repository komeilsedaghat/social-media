# Generated by Django 4.0 on 2022-05-17 07:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_followusermodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='blocked_users',
            field=models.ManyToManyField(blank=True, related_name='blocked', to=settings.AUTH_USER_MODEL),
        ),
    ]
