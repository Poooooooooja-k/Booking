from rest_framework import serializers
from authentication.models import User

class UserSerializer(serializers.ModelField):
    class Meta:
        Model=User
        fields="__all__"