from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from booking.models import FitnessClass
from booking.serializers.fitness_class import FitnessClassSerializer


class CreateFitnessClassAPIView(GenericAPIView):
    """
    API view to create a new fitness class.

    Method:
        - POST

    Request Body:
        - Fields required by FitnessClassSerializer (e.g. name, description, schedule, etc.)

    Responses:
        - 201 Created: Fitness class created successfully, returns the created data.
        - 400 Bad Request: If the request data is invalid.
    """

    serializer_class = FitnessClassSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Fitness Class created successfully!",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class ListFitnessClassAPIView(GenericAPIView):
    """
    API view to list all active (non-deleted) fitness classes.

    Method:
        - GET

    Response:
        - 200 OK: Returns a list of fitness classes that are not soft-deleted.
    """

    serializer_class = FitnessClassSerializer

    def get(self, request):
        fitness_classes = FitnessClass.objects.filter(is_deleted=False)
        serializer = self.get_serializer(fitness_classes, many=True)
        return Response(
            {
                "message": "Fitness classes retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class RetrieveFitnessClassAPIView(GenericAPIView):
    """
    API view to retrieve a fitness class by ID if it is not soft-deleted.

    Method:
        - POST

    Query Parameters:
        - fitness_id (required): ID of the fitness class to retrieve.

    Responses:
        - 200 OK: Fitness class retrieved successfully.
        - 400 Bad Request: fitness_id query parameter is missing.
        - 404 Not Found: Fitness class with given ID does not exist or has been soft-deleted.
    """

    serializer_class = FitnessClassSerializer

    def get(self, request):
        fitness_id = request.GET.get("fitness_id")

        if not fitness_id:
            return Response(
                {"error": "fitness_id query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            fitness_obj = FitnessClass.objects.get(id=fitness_id, is_deleted=False)
        except FitnessClass.DoesNotExist:
            return Response(
                {"error": "Fitness class not found or has been deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(fitness_obj)
        return Response(
            {
                "message": "Fitness class retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class UpdateFitnessClassAPIView(GenericAPIView):
    """
    API view to update a fitness class by ID.

    Methods:
        - PUT: Full update of the fitness class.
        - PATCH: Partial update of the fitness class.

    Query Parameters:
        - fitness_id (required): ID of the fitness class to update.

    Responses:
        - 200 OK: Fitness class updated successfully.
        - 400 Bad Request: fitness_id is missing or validation errors in update data.
        - 404 Not Found: Fitness class with given ID does not exist or has been soft-deleted.
    """

    serializer_class = FitnessClassSerializer

    def put(self, request):
        fitness_id = request.GET.get("fitness_id")
        if not fitness_id:
            return Response(
                {"error": "fitness_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            fitness_obj = FitnessClass.objects.get(id=fitness_id, is_deleted=False)
        except FitnessClass.DoesNotExist:
            return Response(
                {"error": "Fitness class not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(fitness_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Fitness class updated successfully.",
                    "data": serializer.data,
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        fitness_id = request.GET.get("fitness_id")
        if not fitness_id:
            return Response(
                {"error": "fitness_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            fitness_obj = FitnessClass.objects.get(id=fitness_id, is_deleted=False)
        except FitnessClass.DoesNotExist:
            return Response(
                {"error": "Fitness class not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(fitness_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Fitness class partially updated.", "data": serializer.data}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteFitnessClassAPIView(GenericAPIView):
    """
    API view to soft delete a fitness class by setting `is_deleted=True`.

    Method:
        - DELETE: Soft deletes the fitness class identified by `fitness_id`.

    Query Parameters:
        - fitness_id (required): ID of the fitness class to soft delete.

    Responses:
        - 204 No Content: Fitness class was soft deleted successfully.
        - 400 Bad Request: fitness_id query parameter is missing.
        - 404 Not Found: Fitness class not found or already deleted.
    """

    serializer_class = FitnessClassSerializer

    def delete(self, request):
        fitness_id = request.GET.get("fitness_id")

        if not fitness_id:
            return Response(
                {"error": "fitness_id is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            fitness_obj = FitnessClass.objects.get(id=fitness_id, is_deleted=False)
            fitness_obj.is_deleted = True
            fitness_obj.save()
        except FitnessClass.DoesNotExist:
            return Response(
                {"error": "Fitness class not found or already deleted."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            {"message": "Fitness class soft-deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
