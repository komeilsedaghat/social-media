# Generated by Django 4.0 on 2022-05-03 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_ipadressmodel_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='NameModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fuck', models.CharField(max_length=200)),
            ],
        ),
    ]
