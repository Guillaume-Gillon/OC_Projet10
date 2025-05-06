from django.contrib import admin

from .models import ProjectsModel, IssuesModel, CommentsModel, ContributorModel


class ProjectsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "author", "created_time")


class IssuesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "created_time")


class CommentsAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "created_time")


class ContributorAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "project")


admin.site.register(ProjectsModel, ProjectsAdmin)
admin.site.register(IssuesModel, IssuesAdmin)
admin.site.register(CommentsModel, CommentsAdmin)
admin.site.register(ContributorModel, ContributorAdmin)
