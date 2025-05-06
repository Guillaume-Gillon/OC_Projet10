from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import ContributorModel, ProjectsModel, IssuesModel, CommentsModel

User = get_user_model()


def format_created_time():
    return serializers.DateTimeField(format="%d/%m/%Y - %H:%M", read_only=True)


class DisplayUsernameSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "username")


class DisplayProjectNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectsModel
        fields = ("id", "name")


class DisplayIssueNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssuesModel
        fields = ("id", "title")


class ContributorMixin:
    def get_actual_contributors(self, instance):
        """
        Récupère et sérialise les contributeurs d'un projet.
        """
        queryset = instance.contributors_users.all().select_related("user")
        serializer = DisplayUsernameSerializer(
            [contributor.user for contributor in queryset], many=True
        )
        return serializer.data


class AuthorMixin:
    def get_author(self, instance):
        """
        Récupère et sérialise les auteurs d'un projet.
        """
        serializer = DisplayUsernameSerializer(instance.author)
        return serializer.data


class ProjectSerializer(AuthorMixin, ContributorMixin, serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    contributors = serializers.MultipleChoiceField(choices=[], write_only=True)
    nb_contributors = serializers.SerializerMethodField()
    actual_contributors = serializers.SerializerMethodField()
    created_time = format_created_time()

    class Meta:
        model = ProjectsModel
        fields = (
            "id",
            "name",
            "description",
            "type",
            "nb_contributors",
            "actual_contributors",
            "author",
            "contributors",
            "created_time",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["contributors"].choices = [
            (user.id, user.username)
            for user in User.objects.exclude(id=1).exclude(id=2)
        ]

    def get_nb_contributors(self, instance):
        queryset = instance.contributors_users.all().select_related("user")
        nb_contributors = queryset.count()
        return nb_contributors

    def create(self, validated_data):
        contributors_ids = validated_data.pop("contributors", None)
        actual_user = self.context["request"].user
        project = ProjectsModel.objects.create(author=actual_user, **validated_data)

        for user_id in contributors_ids:
            user = User.objects.get(id=user_id)
            ContributorModel.objects.create(user=user, project=project)

        if not ContributorModel.objects.filter(
            user=actual_user, project=project
        ).exists():
            ContributorModel.objects.create(user=actual_user, project=project)
        return project


class ProjectUpdateSerializer(ContributorMixin, serializers.ModelSerializer):

    add_contributor = serializers.MultipleChoiceField(choices=[], write_only=True)
    remove_contributor = serializers.MultipleChoiceField(choices=[], write_only=True)

    class Meta:
        model = ProjectsModel
        fields = (
            "name",
            "description",
            "type",
            "add_contributor",
            "remove_contributor",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        users = [
            (user.id, user.username)
            for user in User.objects.exclude(id=1).exclude(id=2)
        ]
        self.fields["add_contributor"].choices = users
        self.fields["remove_contributor"].choices = users

    def update(self, instance, validated_data):
        validated_data.pop("contributors", None)
        project_instance = super().update(instance, validated_data)
        author = User.objects.get(id=instance.author.id)
        actual_contributors_ids = ContributorModel.objects.filter(
            project=project_instance
        ).values_list("user_id", flat=True)

        if instance.add_contributor is not None:
            for user_id in instance.add_contributor:
                if user_id in actual_contributors_ids:
                    continue
                else:
                    user = User.objects.get(id=user_id)
                    ContributorModel.objects.create(user=user, project=project_instance)

        if instance.remove_contributor is not None:
            for user_id in instance.remove_contributor:
                if user_id in actual_contributors_ids:
                    user = User.objects.get(id=user_id)
                    if not user == author:
                        ContributorModel.objects.filter(
                            user=user, project=project_instance
                        ).delete()

        return instance


class IssueSerializer(AuthorMixin, serializers.ModelSerializer):

    author = serializers.SerializerMethodField()
    project_related = serializers.SerializerMethodField()
    project = serializers.PrimaryKeyRelatedField(
        queryset=ProjectsModel.objects.all(), write_only=True
    )
    created_time = format_created_time()

    class Meta:
        model = IssuesModel
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "tags",
            "status",
            "created_time",
            "author",
            "project_related",
            "project",
        ]

    def get_project_related(self, instance):
        serializer = DisplayProjectNameSerializer(instance.project)
        return serializer.data

    def create(self, validated_data):
        actual_user = self.context["request"].user
        issue = IssuesModel.objects.create(author=actual_user, **validated_data)
        return issue


class IssueUpdateSerializer(AuthorMixin, serializers.ModelSerializer):

    class Meta:
        model = IssuesModel
        fields = (
            "title",
            "description",
            "priority",
            "tags",
            "status",
        )


class CommentSerializer(AuthorMixin, serializers.ModelSerializer):

    issue_link = serializers.SerializerMethodField(read_only=True)
    author = serializers.SerializerMethodField()
    issue_related = serializers.SerializerMethodField()
    issue = serializers.PrimaryKeyRelatedField(
        queryset=IssuesModel.objects.all(), write_only=True
    )
    created_time = format_created_time()

    class Meta:
        model = CommentsModel
        fields = (
            "id",
            "description",
            "issue_link",
            "created_time",
            "author",
            "issue_related",
            "issue",
        )

    def get_issue_link(self, instance):
        return instance.issue_link

    def get_issue_related(self, instance):
        serializer = DisplayIssueNameSerializer(instance.issue)
        return serializer.data

    def create(self, validated_data):
        issue_instance = validated_data.get("issue")
        actual_user = self.context["request"].user
        issue_link = "127.0.0.1:8000/api/display-issues/" + str(issue_instance.id)
        comment = CommentsModel.objects.create(
            author=actual_user, issue_link=issue_link, **validated_data
        )
        return comment


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentsModel
        fields = ("description",)
