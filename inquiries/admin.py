from django.contrib import admin

# Register your models here.
from .models import ContactInquiry, FeedbackInquiry

admin.site.register(ContactInquiry)
admin.site.register(FeedbackInquiry)