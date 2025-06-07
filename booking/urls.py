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
from booking.views.v1.list_booking_of_user import UserBookingsApiView
from booking.views.v1.book_slot import BookClassApiView
from booking.views.v1.list_upcoming_class import UpcomingClassesApiView
from booking.views.v1.cancel_booking import CancelBookingApiView

urlpatterns = [
    path("v1/create_class_type/", CreateClassApiView.as_view()),
    path("v1/list_class/", ListClassApiView.as_view()),
    path("v1/retrive_class/", RetrieveClassApiView.as_view()),
    path("v1/Update_class_type/", UpdateClassApiView.as_view()),
    path("v1/delete_class_type/", DeleteClassApiView.as_view()),
    path(
        "v1/create_fitness_class/",
        CreateFitnessClassAPIView.as_view(),
        name="create-fitness-class",
    ),
    path(
        "v1/list_fitness_class/",
        ListFitnessClassAPIView.as_view(),
        name="list-fitness-classes",
    ),
    path(
        "v1/retrieve_fitness_class/",
        RetrieveFitnessClassAPIView.as_view(),
        name="get-fitness-class",
    ),
    path(
        "v1/update_fitness_class/",
        UpdateFitnessClassAPIView.as_view(),
        name="update-fitness-class",
    ),
    path(
        "v1/delete_fitness_class/",
        DeleteFitnessClassAPIView.as_view(),
        name="delete-fitness-class",
    ),
    path("v1/user_bookings/", UserBookingsApiView.as_view()),
    path("v1/book_slot/", BookClassApiView.as_view()),
    path("v1/list_upcoming_class/", UpcomingClassesApiView.as_view()),
    path("v1/cancel_booking/", CancelBookingApiView.as_view()),
]
