from django.urls import path
from authentication.views.v1.signup import UserSignupApiView
from authentication.views.v1.login import UserLoginApiView
from authentication.views.v1.update_user import UpdateUserApiView,GetUsersApiView,GetUsersApiView,SoftDeleteUserApiView

urlpatterns = [
    path("v1/signup/", UserSignupApiView.as_view()),
    path("v1/login/", UserLoginApiView.as_view()),
    path("v1/update_user/<int:id>/",UpdateUserApiView.as_view()),
    path("v1/user_list/",GetUsersApiView.as_view()),
    path("v1/user_list_by_id/<int:id>/",GetUsersApiView.as_view()),
    path("v1/delete/<int:id>/",SoftDeleteUserApiView.as_view())
]
