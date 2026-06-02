from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import (
    PasswordChangeSerializer,
    PasswordForgotSerializer,
    PasswordResetConfirmSerializer,
    RegisterSerializer,
    UserSerializer,
)
from users.services.password_reset import send_password_reset_email

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully."})


class PasswordForgotView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordForgotSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        response_data = {
            "detail": "If an account with that email exists, password reset instructions have been sent."
        }

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(response_data)

        uid, token, reset_url = send_password_reset_email(user)

        if settings.DEBUG:
            response_data["resetUrl"] = reset_url
            response_data["uid"] = uid
            response_data["token"] = token

        return Response(response_data)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Password has been reset. You can log in with your new password."},
            status=status.HTTP_200_OK,
        )
