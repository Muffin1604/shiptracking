from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import (
    MeView,
    PasswordChangeView,
    PasswordForgotView,
    PasswordResetConfirmView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token-obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("password/change/", PasswordChangeView.as_view(), name="password-change"),
    path("password/forgot/", PasswordForgotView.as_view(), name="password-forgot"),
    path("password/reset/", PasswordResetConfirmView.as_view(), name="password-reset"),
]
