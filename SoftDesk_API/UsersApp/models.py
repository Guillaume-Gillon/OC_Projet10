from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import PermissionDenied

from datetime import date

ADMIN_USER_ID = 1


class UserModel(AbstractUser):
    birthdate = models.DateField()
    RGPD_CHOICES = (("OUI", "OUI"), ("NON", "NON"))
    can_be_contacted = models.CharField(max_length=3, choices=RGPD_CHOICES)
    can_data_be_shared = models.CharField(max_length=3, choices=RGPD_CHOICES)

    def delete(self, *args, **kwargs):
        if self.id == ADMIN_USER_ID:
            raise PermissionDenied(
                "La suppression de l'administrateur n'est pas autorisée."
            )
        super().delete(*args, **kwargs)
