from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from booking.models import Booking
from booking.serializers.booking import BookingSerializer
import logging

logger = logging.getLogger(__name__)

class UserBookingsApiView(ListAPIView):
    """
    API view to list all bookings for a specific user based on their email.
    Accepts 'email' as a query parameter.
    """
    serializer_class = BookingSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')

        if not email:
            logger.warning("UserBookingsApiView: Missing 'email' query parameter.")
            return Booking.objects.none()

        bookings = Booking.objects.filter(client_email=email)
        logger.info(f"UserBookingsApiView: {bookings.count()} bookings found for email: {email}")
        return bookings
