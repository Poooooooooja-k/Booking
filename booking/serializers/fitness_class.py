from rest_framework import serializers
from booking.models import FitnessClass


class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = "__all__"


class FitnessSerializer(serializers.ModelSerializer):
    """
    Serializer for FitnessClass model to display class details along with
    dynamically calculated available slots.

    Fields:
        - id: FitnessClass primary key
        - class_name: Name of the class type (from related ClassType model)
        - start_time: Class start datetime
        - end_time: Class end datetime
        - instructor_name: Name of the instructor
        - available_slots: Number of remaining available slots for booking
    """

    class_name = serializers.CharField(source="class_type.name")
    available_slots = serializers.SerializerMethodField()

    class Meta:
        model = FitnessClass
        fields = [
            "id",
            "class_name",
            "start_time",
            "end_time",
            "instructor_name",
            "available_slots",
        ]

    def get_available_slots(self, obj):
        return obj.capacity - obj.bookings.filter(is_cancelled=False).count()
