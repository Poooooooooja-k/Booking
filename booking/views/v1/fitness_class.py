from rest_framework import generics, status
from rest_framework.response import Response
from booking.models import FitnessClass
from booking.serializers.fitness_class import FitnessClassSerializer


class CreateFitnessClassAPIView(generics.CreateAPIView):
    """
    Create a new fitness class.
    """

    serializer_class = FitnessClassSerializer
    queryset = FitnessClass.objects.all()


class ListFitnessClassAPIView(generics.ListAPIView):
    """
    List all active (non-deleted) fitness classes.
    """

    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        return FitnessClass.objects.filter(is_deleted=False)


class RetrieveFitnessClassAPIView(generics.RetrieveAPIView):
    """
    Retrieve a fitness class by ID if not soft-deleted.
    """

    serializer_class = FitnessClassSerializer
    lookup_field = "id"

    def get_queryset(self):
        return FitnessClass.objects.filter(is_deleted=False)


class UpdateFitnessClassAPIView(generics.UpdateAPIView):
    """
    Update a fitness class.
    """

    serializer_class = FitnessClassSerializer
    lookup_field = "id"

    def get_queryset(self):
        return FitnessClass.objects.filter(is_deleted=False)


class DeleteFitnessClassAPIView(generics.DestroyAPIView):
    """
    Soft delete a fitness class.
    """

    serializer_class = FitnessClassSerializer
    lookup_field = "id"

    def get_queryset(self):
        return FitnessClass.objects.filter(is_deleted=False)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(
            {"message": "Fitness class soft-deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
