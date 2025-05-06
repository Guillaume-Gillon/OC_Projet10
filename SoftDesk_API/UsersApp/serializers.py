from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from datetime import date
import re

User = get_user_model()


def format_birthdate():
    return serializers.DateField(
        format="%d/%m/%Y", input_formats=["%d/%m/%Y"], read_only=True
    )


def validation_password(data):
    if "password" in data and data["password"]:
        if "confirmation_password" not in data or not data["confirmation_password"]:
            raise serializers.ValidationError(
                "Le champ de confirmation du mot de passe est requis si vous fournissez un mot de passe."
            )

        if data["password"] != data["confirmation_password"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")

        if len(data["password"]) < 12:
            raise ValidationError(
                ("Le mot de passe doit contenir au moins 12 caractères.")
            )

        if not re.search(r"[A-Z]", data["password"]):
            raise ValidationError(
                ("Le mot de passe doit contenir au moins une lettre majuscule.")
            )

        if not re.search(r"[a-z]", data["password"]):
            raise ValidationError(
                ("Le mot de passe doit contenir au moins une lettre minuscule.")
            )

        if not re.search(r"[0-9]", data["password"]):
            raise ValidationError(
                ("Le mot de passe doit contenir au moins un chiffre.")
            )

    elif "confirmation_password" in data and data["confirmation_password"]:
        if "password" not in data or not data["password"]:
            raise serializers.ValidationError(
                "Vous avez fourni une confirmation de mot de passe sans fournir le nouveau mot de passe."
            )


class UserUpdateSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True
    )
    confirmation_password = serializers.CharField(
        write_only=True, required=False, allow_null=True, allow_blank=True
    )

    birthdate = serializers.DateField(
        format="%d/%m/%Y", input_formats=["%d/%m/%Y", "%Y-%m-%d"], read_only=True
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "birthdate",
            "password",
            "confirmation_password",
            "can_be_contacted",
            "can_data_be_shared",
        )

    def validate(self, data):
        validation_password(data)
        return data

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirmation_password = serializers.CharField(write_only=True, required=True)

    birthdate = serializers.DateField(
        format="%d/%m/%Y", input_formats=["%d/%m/%Y", "%Y-%m-%d"]
    )

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "birthdate",
            "password",
            "confirmation_password",
            "can_be_contacted",
            "can_data_be_shared",
        )

    def validate_birthdate(self, value):
        today = date.today()
        age = (
            today.year
            - value.year
            - ((today.month, today.day) < (value.month, value.day))
        )
        if age < 15:
            raise serializers.ValidationError(
                "Vous devez avoir au moins 15 ans pour vous inscrire."
            )
        return value

    def validate(self, data):
        validation_password(data)
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("confirmation_password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
