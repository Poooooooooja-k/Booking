from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from booking.models import Booking
from core.decorators.token_required import token_required
import logging

logger = logging.getLogger(__name__)

class CancelBookingApiView(GenericAPIView):
    """
    API endpoint to cancel a user's booking.
    Token required. Cancels booking by ID if it belongs to the user.
    """
    @token_required
    def post(self, request):
        booking_id = request.GET.get("booking_id")
        email = request.email  

        if not booking_id:
            return Response({"error": "Missing booking_id"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            booking = Booking.objects.get(id=booking_id, client_email=email, is_cancelled=False)
        except Booking.DoesNotExist:
            logger.warning(f"Cancel failed: Booking not found or already cancelled for user {email}")
            return Response({"error": "Booking not found or already cancelled"}, status=status.HTTP_404_NOT_FOUND)

        booking.is_cancelled = True
        booking.save()

        logger.info(f"Booking cancelled: ID={booking_id}, Email={email}")
        return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)
