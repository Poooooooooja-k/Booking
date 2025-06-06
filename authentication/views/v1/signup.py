from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from authentication.serializer.signup import UserSignupSerializer

class UserSignupApiView(GenericAPIView):
    """
    API view to handle user registration.

    Accepts user data including name, email, password, and confirm_password.
    Validates password match and strength.
    Hashes the password before saving to the database.

    Returns:
        201 Created on successful registration.
        400 Bad Request with validation errors otherwise.
    """
    serializer_class = UserSignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(
                {"message": "User registered successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
