# Generated by Django 4.0 on 2022-05-07 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_commentmodel_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentmodel',
            name='status',
            field=models.CharField(choices=[('A', 'Accepted'), ('i', 'Investigation'), ('R', 'Rejected')], max_length=1),
        ),
    ]