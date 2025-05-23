# Generated by Django 5.2 on 2025-05-06 08:15

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CommentsModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=1000)),
                ('issue_link', models.CharField(max_length=200)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContributorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='IssuesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('priority', models.CharField(choices=[('HIGH', 'HIGH'), ('MEDIUM', 'MEDIUM'), ('LOW', 'LOW')], max_length=20)),
                ('tags', models.CharField(choices=[('BUG', 'BUG'), ('FEATURE', 'FEATURE'), ('TASK', 'TASK')], max_length=20)),
                ('status', models.CharField(choices=[('ToDo', 'ToDo'), ('In Progress', 'In Progress'), ('Finished', 'Finished')], default='ToDo', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('type', models.CharField(choices=[('back end', 'back end'), ('front end', 'front end'), ('iOS', 'iOS'), ('Android', 'Android')], max_length=20)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
