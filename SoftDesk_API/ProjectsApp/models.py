from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

import uuid

User = get_user_model()


def get_deleted_user():
    return User.objects.get(username="deleted_user")


class ContributorModel(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributions"
    )
    project = models.ForeignKey(
        "ProjectsModel", on_delete=models.CASCADE, related_name="contributors_users"
    )

    class Meta:
        unique_together = ("user", "project")


class ProjectsModel(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=2
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    TYPE_CHOICES = (
        ("back end", "back end"),
        ("front end", "front end"),
        ("iOS", "iOS"),
        ("Android", "Android"),
    )
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class IssuesModel(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=2
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    project = models.ForeignKey(
        "ProjectsModel", on_delete=models.CASCADE, related_name="issues"
    )
    created_time = models.DateTimeField(auto_now_add=True)

    PRIORITY_CHOICES = (
        ("HIGH", "HIGH"),
        ("MEDIUM", "MEDIUM"),
        ("LOW", "LOW"),
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)

    TAGS_CHOICES = (
        ("BUG", "BUG"),
        ("FEATURE", "FEATURE"),
        ("TASK", "TASK"),
    )
    tags = models.CharField(max_length=20, choices=TAGS_CHOICES)

    STATUS_CHOICES = (
        ("ToDo", "ToDo"),
        ("In Progress", "In Progress"),
        ("Finished", "Finished"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ToDo")

    def __str__(self):
        return self.title


class CommentsModel(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, default=2
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.CharField(max_length=1000)
    issue_link = models.CharField(max_length=200)
    created_time = models.DateTimeField(auto_now_add=True)
    issue = models.ForeignKey(
        "IssuesModel", on_delete=models.CASCADE, related_name="comments"
    )
