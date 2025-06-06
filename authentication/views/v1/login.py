from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
import datetime
from django.conf import settings
from authentication.serializer.login import UserLoginSerializer


class UserLoginApiView(GenericAPIView):
    """
    API view for user login.

    Accepts:
        - email: User's registered email address
        - password: User's password

    Returns:
        - access_token: JWT access token (custom signed with expiry)
        - refresh_token: JWT refresh token (from SimpleJWT)
        - user_id: ID of the logged-in user
        - email: User's email
        - message: Success message

    HTTP Methods:
        - POST

    Response Codes:
        - 201 Created: Login successful
        - 400 Bad Request: Validation failed (invalid email/password)
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                {"message": "Validation Failed", "errors": e.detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        secret_key = settings.JWT_SECRET_KEY
        algorithm = settings.ALGORITHM
        access_expiry = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token_payload = {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(minutes=access_expiry),
            "iat": datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload, secret_key, algorithm=algorithm)

        return Response(
            {
                "message": "User Logged in successfully!!",
                "user_id": user.id,
                "email": user.email,
                "access_token": access_token,
                "refresh_token": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )
