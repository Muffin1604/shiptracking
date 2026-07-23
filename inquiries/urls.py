from django.urls import path

from .views import ContactInquiryView, FeedbackInquiryView

urlpatterns = [
    path("contact/", ContactInquiryView.as_view(), name="contact-inquiry"),
    path("feedback/", FeedbackInquiryView.as_view(), name="feedback-inquiry"),
]
