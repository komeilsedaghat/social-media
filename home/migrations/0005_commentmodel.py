# Generated by Django 4.0 on 2022-05-06 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_profile_img'),
        ('home', '0004_alter_postmodel_author_alter_postmodel_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=400)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('A', 'Accepted'), ('R', 'Rejected')], max_length=1)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
