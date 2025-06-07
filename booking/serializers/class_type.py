from rest_framework import serializers
from booking.models import ClassType


class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassType
        fields = "__all__"
