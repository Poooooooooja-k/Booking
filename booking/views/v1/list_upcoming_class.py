from rest_framework.generics import ListAPIView
from booking.models import FitnessClass
from booking.serializers.fitness_class import FitnessSerializer
from django.utils import timezone


class UpcomingClassesApiView(ListAPIView):
    """
    API view to retrieve a list of upcoming fitness classes.

    Returns all FitnessClass instances where the start_time is greater than or equal
    to the current time (upcoming classes) and that are not marked as deleted.

    Uses the FitnessSerializer to serialize the fitness class data.
    """

    serializer_class = FitnessSerializer

    def get_queryset(self):
        """
        Get the queryset of upcoming fitness classes.

        Filters FitnessClass objects to include only those with:
        - start_time greater than or equal to the current datetime
        - is_deleted flag set to False

        Returns:
            QuerySet: Filtered queryset of FitnessClass instances.
        """
        return FitnessClass.objects.filter(
            start_time__gte=timezone.now(), is_deleted=False
        )
