from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from authentication.models import User


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Handles user registration:
    - Ensures password and confirm_password match.
    - Checks password length (minimum 6 characters).
    - Hashes the password before storing.
    - Only the hashed password is saved to the database.
    """

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "age",
            "phone_number",
            "password",
            "confirm_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        if len(password) < 6:
            raise serializers.ValidationError(
                "Password must be at least 6 characters long."
            )

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        validated_data["password"] = make_password(validated_data["password"])

        return super().create(validated_data)
