from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

from authentication.serializer.user import UserSerializer
from authentication.models import User
from core.decorators.token_required import token_required


class UpdateUserApiView(GenericAPIView):
    """
    API view to update an existing user.

    Methods:
        - PUT: Full update of the user data.
        - PATCH: Partial update of the user data.

    URL Parameter:
        - id (int): Primary key of the user to update.

    Authentication:
        - Requires token authentication (@token_required decorator).
    """

    serializer_class = UserSerializer

    @token_required
    def put(self, request, id):
        """
        Handle full update of a user instance by ID.
        """
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Deserialize and validate incoming data
        serializer = self.get_serializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def patch(self, request, id):
        """
        Handle partial update of a user instance by ID.
        """
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User partially updated", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUsersApiView(GenericAPIView):
    """
    API view to list all active (non-deleted) users.

    Method:
        - GET: Retrieve all users where `is_deleted=False`.

    Authentication:
        - Requires token authentication (@token_required decorator).
    """

    serializer_class = UserSerializer

    @token_required
    def get(self, request):
        users = User.objects.filter(is_deleted=False)
        serializer = self.get_serializer(users, many=True)
        return Response(
            {"message": "User list retrieved successfully.", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class GetUserByIdApiView(GenericAPIView):
    """
    API view to retrieve a single user by ID.

    Method:
        - GET: Retrieve a user by ID from query parameters.

    Query Parameter:
        - user_id (int): ID of the user to retrieve.

    Authentication:
        - Requires token authentication (@token_required decorator).
    """

    serializer_class = UserSerializer

    @token_required
    def get(self, request, *args, **kwargs):
        user_id = request.GET.get("user_id")
        if not user_id:
            return Response(
                {"error": "User ID not provided."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id, is_deleted=False)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(user)
        return Response(
            {"message": "User retrieved successfully.", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class SoftDeleteUserApiView(GenericAPIView):
    """
    API view to soft delete the authenticated user by setting `is_deleted=True`.

    Method:
        - PATCH: Soft delete the user based on user ID from the token.

    Authentication:
        - Requires token authentication (@token_required decorator).
        - User ID is extracted from the token (`request.user_id`).
    """

    serializer_class = UserSerializer

    @token_required
    def patch(self, request):
        # Extract user_id from authenticated token
        user_id = request.user_id
        if not user_id:
            return Response(
                {"error": "User ID not found in token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_obj = User.objects.get(id=user_id, is_deleted=False)
            user_obj.is_deleted = True
            user_obj.save()
        except User.DoesNotExist:
            return Response(
                {"error": "User not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"message": "User deleted successfully."},
            status=status.HTTP_200_OK,
        )
