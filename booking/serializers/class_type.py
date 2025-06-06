from rest_framework import serializers
from booking.models import ClassType

class ClassTypeSerializer(serializers.ModelSerializer):
    class Meta:
        Model="ClassType"
        fields="__all__"