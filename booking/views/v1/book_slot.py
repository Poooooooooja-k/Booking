from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from booking.models import FitnessClass, Booking
from core.decorators.token_required import token_required
import logging

logger = logging.getLogger(__name__)


class BookClassApiView(GenericAPIView):
    """
    API endpoint to book a fitness class for an authenticated user.

    This view handles POST requests to create a booking for a fitness class.
    The user must provide the class ID and their name in the request body.
    The user's email is extracted from the authentication token.

    Workflow:
    1. Validate that the requested fitness class exists and is not soft-deleted.
    2. Check if the class is already full and reject the booking if so.
    3. Prevent duplicate bookings by the same user for the same class.
    4. If all checks pass, create a new booking.
    5. Return appropriate success or error responses.

    Authentication:
    - Requires a valid token (enforced by the `@token_required` decorator).

    Request body parameters:
    - class_id: ID of the fitness class to book.
    - client_name: Name of the client booking the class.

    Response:
    - 201 Created on successful booking.
    - 400 Bad Request with error details for invalid requests or business rule violations.
    """

    @token_required
    def post(self, request):
        class_id = request.data.get("class_id")
        name = request.data.get("client_name")
        email = request.email

        logger.info(
            f"Booking attempt: class_id={class_id}, client_name={name}, client_email={email}"
        )

        try:
            fitness_class = FitnessClass.objects.get(id=class_id, is_deleted=False)
            logger.debug(f"FitnessClass found: {fitness_class}")
        except FitnessClass.DoesNotExist:
            logger.warning(
                f"Booking failed: FitnessClass with id={class_id} not found or deleted."
            )
            return Response(
                {"error": "Class not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        if fitness_class.is_full():
            logger.info(f"Booking failed: Class {fitness_class} is full.")
            return Response(
                {"error": "Class is already full"}, status=status.HTTP_400_BAD_REQUEST
            )
        if Booking.objects.filter(
            fitness_class=fitness_class, client_email=email
        ).exists():
            logger.warning(
                f"Duplicate booking attempt by {email} for class {fitness_class}"
            )
            return Response(
                {"error": "You have already booked this class."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        booking = Booking.objects.create(
            fitness_class=fitness_class, client_name=name, client_email=email
        )
        logger.info(f"Booking successful: {booking}")

        return Response(
            {"message": "Booking successful"}, status=status.HTTP_201_CREATED
        )
