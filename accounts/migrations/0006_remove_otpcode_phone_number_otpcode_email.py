# Generated by Django 4.0 on 2022-05-13 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_otpcode_user_tfa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='otpcode',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='otpcode',
            name='email',
            field=models.EmailField(default=None, max_length=254),
            preserve_default=False,
        ),
    ]
