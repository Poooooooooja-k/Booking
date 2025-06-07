from django.db import models
from core.models import BaseModel

# Create your models here.


class User(BaseModel):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.email
