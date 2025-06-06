from rest_framework import serializers
from authentication.models import User
from django.contrib.auth.hashers import check_password

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login authentication.

    Fields:
        - email: User's registered email (required)
        - password: User's password (required)

    Validation:
        - Checks if the email exists in the system.
        - Validates that the password matches the hashed password.
        - Ensures the user account is active.

    On success:
        - Returns the authenticated user in `data["user"]` for use in the view.

    Raises:
        - ValidationError with specific messages for:
            - Invalid email
            - Incorrect password
            - Inactive account
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email is not registered."})

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user": "Invalid user for this email."})

        if not check_password(password, user.password):
            raise serializers.ValidationError({"password": "Invalid password."})

        if not user.is_active:
            raise serializers.ValidationError({"email": "User account is inactive."})

        data["user"] = user
        return data
