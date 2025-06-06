from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from booking.models import FitnessClass, Booking
import logging

logger = logging.getLogger(__name__)

class BookClassApiView(GenericAPIView):
    """
    API endpoint to book a fitness class.
    """
    def post(self, request):
        class_id = request.data.get("class_id")
        name = request.data.get("client_name")
        email = request.data.get("client_email")

        logger.info(f"Booking attempt: class_id={class_id}, client_name={name}, client_email={email}")

        try:
            fitness_class = FitnessClass.objects.get(id=class_id, is_deleted=False)
            logger.debug(f"FitnessClass found: {fitness_class}")
        except FitnessClass.DoesNotExist:
            logger.warning(f"Booking failed: FitnessClass with id={class_id} not found or deleted.")
            return Response(
                {"error": "Class not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        if fitness_class.is_full():
            logger.info(f"Booking failed: Class {fitness_class} is full.")
            return Response(
                {"error": "Class is already full"}, status=status.HTTP_400_BAD_REQUEST
            )
        if Booking.objects.filter(fitness_class=fitness_class, client_email=email).exists():
            logger.warning(f"Duplicate booking attempt by {email} for class {fitness_class}")
            return Response(
                {"error": "You have already booked this class."}, status=status.HTTP_400_BAD_REQUEST
            )

        booking = Booking.objects.create(
            fitness_class=fitness_class, client_name=name, client_email=email
        )
        logger.info(f"Booking successful: {booking}")

        return Response(
            {"message": "Booking successful"}, status=status.HTTP_201_CREATED
        )
