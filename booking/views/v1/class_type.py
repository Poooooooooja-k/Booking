from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from booking.models import ClassType
from booking.serializers.class_type import ClassTypeSerializer
from core.decorators.token_required import token_required


class CreateClassApiView(GenericAPIView):
    """
    API view to create a new class type.

    Method:
        - POST

    Request Body:
        - name: string (required)
        - description: string (optional)

    Response:
        - 201 Created: On successful creation of class type
        - 400 Bad Request: If validation fails
    """

    serializer_class = ClassTypeSerializer

    @token_required
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Class type created successfully!",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ListClassApiView(GenericAPIView):
    """
    API view to list all active (non-deleted) class types.

    Method:
        - GET

    Response:
        - 200 OK: Returns a list of class types
    """

    serializer_class = ClassTypeSerializer

    @token_required
    def get(self, request):
        class_types = ClassType.objects.filter(is_deleted=False)
        serializer = self.get_serializer(class_types, many=True)
        return Response(
            {"message": "Class types retrieved successfully.", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class RetrieveClassApiView(GenericAPIView):
    """
    API view to retrieve a class type by ID if it is not soft-deleted.

    Method:
        - POST

    Query Parameter:
        - class_id: int (required)

    Responses:
        - 200 OK: Returns the class type data
        - 400 Bad Request: If class_id is not provided
        - 404 Not Found: If the class type does not exist or is soft-deleted
    """

    serializer_class = ClassTypeSerializer

    @token_required
    def get(self, request):
        class_id = request.GET.get("class_id")

        if not class_id:
            return Response(
                {"error": "class_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            class_obj = ClassType.objects.get(id=class_id, is_deleted=False)
        except ClassType.DoesNotExist:
            return Response(
                {"error": "Class type not found or has been deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(class_obj)
        return Response(
            {"message": "Class type retrieved successfully.", "data": serializer.data},
            status=status.HTTP_200_OK,
        )


class UpdateClassApiView(GenericAPIView):
    """
    API view to update a class type by ID.

    Methods:
        - PUT: Full update of the class type.
        - PATCH: Partial update of the class type.

    Query Parameter:
        - class_id: int (required)

    Responses:
        - 200 OK: Returns updated class type data on success.
        - 400 Bad Request: If 'class_id' is missing or data is invalid.
        - 404 Not Found: If the class type does not exist or is soft-deleted.
    """

    serializer_class = ClassTypeSerializer

    @token_required
    def put(self, request):
        class_id = request.GET.get("class_id")
        if not class_id:
            return Response(
                {"error": "class_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            class_obj = ClassType.objects.get(id=class_id, is_deleted=False)
        except ClassType.DoesNotExist:
            return Response(
                {"error": "Class type not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(class_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Class type updated successfully.", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @token_required
    def patch(self, request):
        class_id = request.GET.get("class_id")
        if not class_id:
            return Response(
                {"error": "class_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            class_obj = ClassType.objects.get(id=class_id, is_deleted=False)
        except ClassType.DoesNotExist:
            return Response(
                {"error": "Class type not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(class_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Class type partially updated.", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteClassApiView(GenericAPIView):
    """
    API view to soft delete a class type by setting `is_deleted=True`.

    Method:
        - DELETE

    Query Parameter:
        - class_id: int (required)

    Responses:
        - 204 No Content: Successfully soft-deleted the class type.
        - 400 Bad Request: If 'class_id' query parameter is missing.
        - 404 Not Found: If the class type does not exist or is already deleted.
    """

    serializer_class = ClassTypeSerializer

    @token_required
    def delete(self, request):
        class_id = request.GET.get("class_id")

        if not class_id:
            return Response(
                {"error": "class_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            class_obj = ClassType.objects.get(id=class_id, is_deleted=False)
            class_obj.is_deleted = True
            class_obj.save()
        except ClassType.DoesNotExist:
            return Response(
                {"error": "Class type not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"message": "Class type soft-deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
