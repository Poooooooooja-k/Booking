from rest_framework import generics, status
from rest_framework.response import Response
from booking.models import ClassType
from booking.serializers.class_type import ClassTypeSerializer


class CreateClassApiView(generics.CreateAPIView):
    """
    API view to create a new class type.

    Method:
        - POST

    Request Body:
        - name: string
        - description: string (optional)

    Response:
        - 201 Created with the created class data
    """
    queryset = ClassType.objects.filter(is_deleted=False)
    serializer_class = ClassTypeSerializer


class ListClassApiView(generics.ListAPIView):
    """
    API view to list all class types.

    Method:
        - GET

    Response:
        - 200 OK with list of class types
    """
    queryset = ClassType.objects.filter(is_deleted=False)
    serializer_class = ClassTypeSerializer


class RetrieveClassApiView(generics.RetrieveAPIView):
    """
    API view to retrieve a class type by ID.

    Method:
        - GET

    URL Params:
        - id: int

    Response:
        - 200 OK with class data
        - 404 Not Found if ID is invalid
    """
    queryset = ClassType.objects.filter(is_deleted=False)
    serializer_class = ClassTypeSerializer
    lookup_field = 'id'


class UpdateClassApiView(generics.UpdateAPIView):
    """
    API view to update a class type by ID.

    Method:
        - PUT / PATCH

    URL Params:
        - id: int

    Request Body:
        - Any field to be updated (e.g. name, description)

    Response:
        - 200 OK with updated class data
        - 400 Bad Request / 404 Not Found
    """
    queryset = ClassType.objects.filter(is_deleted=False)
    serializer_class = ClassTypeSerializer
    lookup_field = 'id'



class DeleteClassApiView(generics.DestroyAPIView):
    """
    Soft delete a class type by setting is_deleted = True.
    """
    serializer_class = ClassTypeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return ClassType.objects.filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(
            {"message": "Class type soft-deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )

