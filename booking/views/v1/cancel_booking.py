from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from booking.models import Booking
from core.decorators.token_required import token_required
import logging

logger = logging.getLogger(__name__)


class CancelBookingApiView(GenericAPIView):
    """
    API endpoint to allow authenticated users to cancel their booking.

    This endpoint requires a valid authentication token and expects a
    `booking_id` as a query parameter. It verifies that the booking exists,
    belongs to the authenticated user (based on email extracted from the token),
    and is not already cancelled before marking it as cancelled.

    Method:
        POST

    Query Parameters:
        - booking_id: ID of the booking to cancel.

    Behavior:
        - Returns 400 Bad Request if `booking_id` is missing.
        - Returns 404 Not Found if the booking does not exist, does not belong to the user,
          or is already cancelled.
        - Marks the booking as cancelled (`is_cancelled=True`) on success.
        - Logs the cancellation activity.

    Response:
        - 200 OK with success message if cancellation is successful.
        - 400 or 404 with error details for failure cases.
    """

    @token_required
    def post(self, request):
        booking_id = request.GET.get("booking_id")
        email = request.email

        if not booking_id:
            return Response(
                {"error": "Missing booking_id"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            booking = Booking.objects.get(
                id=booking_id, client_email=email, is_cancelled=False
            )
        except Booking.DoesNotExist:
            logger.warning(
                f"Cancel failed: Booking not found or already cancelled for user {email}"
            )
            return Response(
                {"error": "Booking not found or already cancelled"},
                status=status.HTTP_404_NOT_FOUND,
            )

        booking.is_cancelled = True
        booking.save()

        logger.info(f"Booking cancelled: ID={booking_id}, Email={email}")
        return Response(
            {"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK
        )
