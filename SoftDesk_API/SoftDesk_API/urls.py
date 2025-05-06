"""
URL configuration for SoftDesk_API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from UsersApp.views import UsersViewset, CreateUsersViewset
from ProjectsApp.views import (
    ProjectsViewset,
    IssuesViewset,
    CommentsViewset,
)

router = routers.SimpleRouter()
router.register("users", UsersViewset, basename="users")
router.register("create-users", CreateUsersViewset, basename="create-users")
router.register("issues", IssuesViewset, basename="issues")
router.register("projects", ProjectsViewset, basename="projects")
router.register("comments", CommentsViewset, basename="comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/", include(router.urls)),
]
