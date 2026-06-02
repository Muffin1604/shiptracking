from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def encode_user_id(user):
    return urlsafe_base64_encode(force_bytes(user.pk))


def build_reset_url(uid, token):
    base = settings.FRONTEND_RESET_PASSWORD_URL.rstrip("/")
    return f"{base}?uid={uid}&token={token}"


def send_password_reset_email(user):
    uid = encode_user_id(user)
    token = default_token_generator.make_token(user)
    reset_url = build_reset_url(uid, token)

    subject = "Reset your Ship Tracking password"
    message = (
        f"Hello,\n\n"
        f"You requested a password reset. Open the link below to set a new password:\n\n"
        f"{reset_url}\n\n"
        f"If you did not request this, you can ignore this email.\n"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return uid, token, reset_url
