from django.urls import path
from authentication.views.v1.signup import UserSignupApiView
from authentication.views.v1.login import UserLoginApiView
from authentication.views.v1.update_user import (
    UpdateUserApiView,
    GetUsersApiView,
    GetUserByIdApiView,
    SoftDeleteUserApiView,
)

urlpatterns = [
    path("v1/signup/", UserSignupApiView.as_view()),
    path("v1/login/", UserLoginApiView.as_view()),
    path("v1/update_user/", UpdateUserApiView.as_view()),
    path("v1/user_list/", GetUsersApiView.as_view()),
    path("v1/user_list_by_id/", GetUserByIdApiView.as_view()),
    path("v1/delete_user/", SoftDeleteUserApiView.as_view()),
]
