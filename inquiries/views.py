from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactInquirySerializer, FeedbackInquirySerializer
# Create your views here.
class ContactInquiryView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ContactInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Inquiry sent successfully",
                "status": "success",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "message": "Inquiry failed",
            "status": "error",
            "errors": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class FeedbackInquiryView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = FeedbackInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Feedback sent successfully",
                "status": "success",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "message": "Feedback failed",
            "status": "error",
            "errors": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)