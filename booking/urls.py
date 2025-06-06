from django.urls import path
from booking.views.v1.class_type import (
    CreateClassApiView,
    ListClassApiView,
    RetrieveClassApiView,
    UpdateClassApiView,
    DeleteClassApiView,
)
from booking.views.v1.fitness_class import (
    CreateFitnessClassAPIView,
    ListFitnessClassAPIView,
    RetrieveFitnessClassAPIView,
    UpdateFitnessClassAPIView,
    DeleteFitnessClassAPIView,
)

urlpatterns = [
    path("v1/create_class_type/", CreateClassApiView.as_view()),
    path("v1/list_class/", ListClassApiView.as_view()),
    path("v1/retrive_class/<int:id>/", RetrieveClassApiView.as_view()),
    path("v1/Update_class_type/<int:id>/", UpdateClassApiView.as_view()),
    path("v1/delete_class_type/<int:id>/", DeleteClassApiView.as_view()),
    path('v1/create_fitness_class/', CreateFitnessClassAPIView.as_view(), name='create-fitness-class'),
    path('v1/list_fitness_class/', ListFitnessClassAPIView.as_view(), name='list-fitness-classes'),
    path('v1/retrieve_fitness_class/<int:id>/', RetrieveFitnessClassAPIView.as_view(), name='get-fitness-class'),
    path('v1/update_fitness_class/<int:id>/', UpdateFitnessClassAPIView.as_view(), name='update-fitness-class'),
    path('v1/delete_fitness_class/<int:id>/', DeleteFitnessClassAPIView.as_view(), name='delete-fitness-class'),
]
