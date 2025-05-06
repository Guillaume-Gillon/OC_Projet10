from django.contrib import admin

from .models import UserModel


class UsersAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "last_login", "is_superuser")


admin.site.register(UserModel, UsersAdmin)
