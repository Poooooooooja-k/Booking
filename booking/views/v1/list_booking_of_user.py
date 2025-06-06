from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from booking.models import Booking
from booking.serializers.booking import BookingSerializer
from core.decorators.token_required import token_required
from authentication.models import User  # import this if needed
import logging

logger = logging.getLogger(__name__)

class UserBookingsApiView(GenericAPIView):
    """
    API view to list all bookings for a specific user.
    Extracts the user email from the token.
    Token must be passed in the request headers.
    """
    serializer_class = BookingSerializer

    @token_required
    def get(self, request):
        user_email = request.email 

        if not user_email:
            logger.warning("UserBookingsApiView: Email not found in token.")
            return Response({"error": "User email not found in token."}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(client_email=user_email)

        logger.info(f"UserBookingsApiView: {bookings.count()} bookings found for {user_email}")

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
