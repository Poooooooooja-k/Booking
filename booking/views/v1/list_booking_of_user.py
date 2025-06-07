from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from booking.models import Booking
from booking.serializers.booking import BookingSerializer
from core.decorators.token_required import token_required
import logging

logger = logging.getLogger(__name__)


class UserBookingsApiView(GenericAPIView):
    """
    API endpoint to retrieve all bookings for the authenticated user.

    This view requires a valid authentication token in the request headers.
    The user's email is extracted from the token and used to filter bookings.

    Method:
        GET

    Authentication:
        Requires a valid token passed in the request headers.
        The token must contain the user's email.

    Behavior:
        - Returns 400 Bad Request if the email is not found in the token.
        - Retrieves all bookings where `client_email` matches the user's email.
        - Returns the list of bookings serialized in the response.

    Response:
        - 200 OK with serialized booking data on success.
        - 400 Bad Request with error message if user email is missing from the token.
    """

    serializer_class = BookingSerializer

    @token_required
    def get(self, request):
        user_email = request.email

        if not user_email:
            logger.warning("UserBookingsApiView: Email not found in token.")
            return Response(
                {"error": "User email not found in token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bookings = Booking.objects.filter(client_email=user_email)

        logger.info(
            f"UserBookingsApiView: {bookings.count()} bookings found for {user_email}"
        )

        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
