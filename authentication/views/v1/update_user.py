from rest_framework import generics, status
from rest_framework.response import Response
from authentication.serializer.user import UserSerializer
from authentication.models import User

class UpdateUserApiView(generics.UpdateAPIView):
    """
    API view to update user details.

    Method: PUT/PATCH
    URL pattern should include the user ID.
    """
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    lookup_field = 'id'


class GetUsersApiView(generics.ListAPIView):
    """
    API view to retrieve a list of all active users.

    Method: GET
    """
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer


class GetUserByIdApiView(generics.RetrieveAPIView):
    """
    API view to retrieve a single user by ID.

    Method: GET
    URL pattern should include the user ID.
    """
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    lookup_field = "id"


class SoftDeleteUserApiView(generics.UpdateAPIView):
    """
    API view to soft-delete a user by setting is_deleted=True.

    Method: PATCH
    URL pattern should include the user ID.
    """
    queryset = User.objects.filter(is_deleted=False)
    serializer_class = UserSerializer
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(
            {"message": "User deleted successfully."},
            status=status.HTTP_200_OK
        )
