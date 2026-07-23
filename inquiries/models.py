from django.db import models

# Create your models here.
class ContactInquiry(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.email}"

class FeedbackInquiry(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    imo_number = models.CharField(max_length=255, null=True, blank=True)
    mmsi_number = models.CharField(max_length=255, null=True, blank=True)
    vessel_name = models.CharField(max_length=255, null=True, blank=True)
    feedback_type = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email}"