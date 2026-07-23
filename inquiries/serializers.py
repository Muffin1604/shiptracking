from rest_framework import serializers
from .models import ContactInquiry

class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = ['first_name', 'last_name', 'email', 'message']