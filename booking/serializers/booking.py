from rest_framework import serializers
from booking.models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source='fitness_class.class_type.name', read_only=True)
    start_time = serializers.DateTimeField(source='fitness_class.start_time', read_only=True)
    end_time = serializers.DateTimeField(source='fitness_class.end_time', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id',
            'client_name',
            'client_email',
            'class_name',
            'start_time',
            'end_time',
            'is_cancelled'
        ]
