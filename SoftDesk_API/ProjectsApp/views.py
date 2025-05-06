from rest_framework.viewsets import ModelViewSet

from django.contrib.auth import get_user_model

from .models import ProjectsModel, IssuesModel, CommentsModel
from .serializers import (
    ProjectSerializer,
    ProjectUpdateSerializer,
    IssueSerializer,
    IssueUpdateSerializer,
    CommentSerializer,
    CommentUpdateSerializer,
)

from PermissionsApp.permissions import (
    IsContributorOrAdmin,
    IsProjectContributorOrAdmin,
    IsIssueFromAuthorizedProjectOrAdmin,
)

User = get_user_model()


class ProjectsViewset(ModelViewSet):
    """
    # Point de terminaison des projets

    Ce point de terminaison permet de **lister** et de **récupérer** des informations sur les projets en autorisant la création d'un nouveau projet et la modification d'un projet existant.

    ### Actions disponibles :

    * `GET /api/projects/` : Récupère la liste de tous les projets (POST).
    * `GET /api/projects/{id}/` : Récupère les détails d'un projet spécifique par son identifiant (PUT - DELETE).

    Pour modifier des informations sur un projet, utilisez le point de terminaison spécifique à l'ID.

    ### Droits d'accès :

    * Lecture/Création : Utilisateurs authentifiés, Administrateur.
    * Modification/Suppression : Utilisateurs authentifiés enregistrés comme contributeurs du projet, Administrateur.
    """

    permission_classes = [IsContributorOrAdmin]

    def get_view_name(self):
        if self.__class__.__name__ == "ProjectsViewset":
            return "Projets"
        return super().get_view_name()

    def get_queryset(self):
        return ProjectsModel.objects.all()

    def get_serializer_class(self):
        if self.action == "update":
            return ProjectUpdateSerializer
        return ProjectSerializer


class IssuesViewset(ModelViewSet):
    """
    # Point de terminaison des tickets

    Ce point de terminaison permet de **lister** et de **récupérer** des informations sur les tickets en autorisant la création d'un nouveau ticket et la modification d'un ticket existant.

    ### Actions disponibles :

    * `GET /api/issues/` : Récupère la liste de tous les tickets. (POST)
    * `GET /api/issues/{id}/` : Récupère les détails d'un ticket spécifique par son identifiant (PUT - DELETE).

    Pour modifier des informations sur un ticket, utilisez le point de terminaison spécifique à l'ID.

    ### Droits d'accès :

    * Lecture : Utilisateurs authentifiés, Administrateur
    * Création : Utilisateurs authentifiés enregistrés comme contributeurs du projet associé, Administrateur.
    * Modification/Suppression : Utilisateur authentifié enregistré comme auteur du ticket, Administrateur.
    """

    permission_classes = [IsProjectContributorOrAdmin]

    def get_view_name(self):
        if self.__class__.__name__ == "ProjectsViewset":
            return "Projets"
        return super().get_view_name()

    def get_queryset(self):
        return IssuesModel.objects.all()

    def get_serializer_class(self):
        if self.action == "update":
            return IssueUpdateSerializer
        return IssueSerializer


class CommentsViewset(ModelViewSet):
    """
    # Point de terminaison des commentaires (POST - PUT - DELETE)

    Ce point de terminaison permet de **lister** et de **récupérer** des informations sur les commentaires en autorisant la création d'un nouveau commentaire et la modification d'un commentaire existant.

    ### Actions disponibles :

    * `GET /api/comments/` : Récupère la liste de tous les commentaires(POST).
    * `GET /api/comments/{id}/` : Récupère les détails d'un commentaire spécifique par son identifiant (PUT - DELETE).

    Pour modifier des informations sur un commentaire, utilisez le point de terminaison spécifique à l'ID.

    ### Droits d'accès :

    * Lecture : Utilisateurs authentifiés, Administrateur
    * Création : Utilisateurs authentifiés enregistrés comme contributeurs du projet associé, Administrateur.
    * Modification/Suppression : Utilisateur authentifié enregistré comme auteur du commentaire, Administrateur.
    """

    permission_classes = [IsIssueFromAuthorizedProjectOrAdmin]

    def get_serializer_class(self):
        if self.action == "update":
            return CommentUpdateSerializer
        return CommentSerializer

    def get_queryset(self):
        return CommentsModel.objects.all()
