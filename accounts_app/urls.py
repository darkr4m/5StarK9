from django.urls import path, include
from .views import UserSignUpView, UserLoginView, UserLogOutView, AdminUserCreate, UserDetailView

urlpatterns = [
    path("register/", UserSignUpView.as_view(), name="user_sign_up"),
    path("auth/login/", UserLoginView.as_view(), name="user_log_in"),
    path("auth/logout/", UserLogOutView.as_view(), name="user_log_out"),
    path("auth/admin", AdminUserCreate.as_view(), name="create_admin_user"),
    path("", UserDetailView.as_view())
]
