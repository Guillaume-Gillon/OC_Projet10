from rest_framework.permissions import BasePermission

from ProjectsApp.models import ContributorModel, ProjectsModel, IssuesModel


# OK
class IsAdminOrNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method == "PUT" or request.method == "DELETE":
            return False
        if request.user.is_superuser:
            return True
        elif request.user and request.user.is_authenticated:
            return False
        if not request.user.is_authenticated:
            if view.action == "create":
                return True
        return False

    def has_object_permission(self, request, view, obj):
        return False


# OK
class IsActualUserOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            return False
        if request.method == "DELETE":
            user_id = view.kwargs.get("pk")
            if user_id is not None and int(user_id) == 2:
                return False
        if not request.user.is_authenticated:
            return False
        elif view.action == "list" and not request.user.is_superuser:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id:
            return True
        return request.user.is_superuser


# OK
class IsContributorOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            return ContributorModel.objects.filter(
                user=request.user, project=obj
            ).exists()
        return False


# OK
class IsProjectContributorOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            project_id = request.data.get("project")
            if project_id is not None and request.user.is_authenticated:
                project = ProjectsModel.objects.get(pk=project_id)
                is_contributor = ContributorModel.objects.filter(
                    user=request.user, project=project
                ).exists()
                if is_contributor or request.user.is_superuser:
                    return True
                else:
                    return False
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.username == obj.author.username:
            return True
        return False


class IsIssueFromAuthorizedProjectOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST":
            issue_id = request.data.get("issue")
            if issue_id is not None and request.user.is_authenticated:
                issue = IssuesModel.objects.get(pk=issue_id)
                is_contributor = ContributorModel.objects.filter(
                    user=request.user, project=issue.project
                ).exists()
                if is_contributor or request.user.is_superuser:
                    return True
                else:
                    return False
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.username == obj.author.username:
            return True
        return False
