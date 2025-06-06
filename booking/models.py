from django.db import models
from core.models import BaseModel
from authentication.models import User
# Create your models here.

class ClassType(BaseModel):
    name=models.CharField(max_length=100)
    description=models.CharField(max_length=255,null=True,blank=True)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class FitnessClass(BaseModel):
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE, related_name='sessions')
    instructor_name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=40)
    is_deleted=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.class_type.name} on {self.start_time.strftime('%Y-%m-%d %H:%M')}"
    
    def available_slots(self):
        return self.capacity - self.bookings.filter(is_cancelled=False).count()

    def is_full(self):
        return self.available_slots() <= 0

class Booking(BaseModel):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    is_cancelled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('fitness_class', 'client_email')

    def __str__(self):
        return f"{self.client_name} - {self.fitness_class}"