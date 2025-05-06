from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model

from .serializers import (
    UserUpdateSerializer,
    UserSerializer,
)

from PermissionsApp.permissions import (
    IsActualUserOrAdmin,
    IsAdminOrNotAuthenticated,
)

from .throttling import CreateUserRateThrottle, UpdatePasswordRateThrottle

User = get_user_model()


class UsersViewset(ModelViewSet):
    """
    # Point de terminaison d'affichage et de modification des utilisateurs (POST interdit)

    Ce point de terminaison permet de **lister** et de **récupérer** des informations sur un utilisateur afin de les modifier ou de les supprimer.

    ### Actions disponibles :

    * `GET /api/users/{id}/` : Récupère la liste des utilisateurs.
    * `GET /api/users/{id}/` : Récupère les détails d'un utilisateur spécifique par son identifiant (PUT - DELETE).

    ### Droits d'accès :

    * Utilisateur actuellement connecté et propriétaire des données demandées.
    * Administrateur.
    """

    permission_classes = [IsActualUserOrAdmin]

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == "update":
            return UserUpdateSerializer
        return UserSerializer

    def get_view_name(self):
        if self.__class__.__name__ == "ModifyUsersViewset":
            return "Gestion des données utilisateur"
        return super().get_view_name()

    def get_throttles(self):
        if self.action == "create":
            return [CreateUserRateThrottle()]
        elif self.action in ["update", "partial_update"]:
            return [UpdatePasswordRateThrottle()]
        return []


class CreateUsersViewset(ModelViewSet):
    """
    # Point de terminaison de création des utilisateurs (POST)

    Ce point de terminaison permet la création d'un nouvel utilisateur.

    ### Actions disponibles :

    * `GET /api/create-users/` : Récupère la liste de tous les utilisateurs (Administrateur uniquement).

    ### Droits d'accès :

    * Utilisateur non connecté.
    * Administrateur.
    """

    permission_classes = [IsAdminOrNotAuthenticated]

    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            user = self.request.user
            return User.objects.filter(username=user.username)

    def get_view_name(self):
        if self.__class__.__name__ == "CreateUsersViewset":
            return "Création d'un nouvel utilisateur"
        return super().get_view_name()
