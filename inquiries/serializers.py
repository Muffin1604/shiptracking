from rest_framework import serializers
from .models import ContactInquiry, FeedbackInquiry

class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = ['first_name', 'last_name', 'email', 'message']

class FeedbackInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackInquiry
        fields = ['name', 'email', 'imo_number', 'mmsi_number', 'vessel_name', 'feedback_type', 'message']