from django.shortcuts import render

# Create your views here.
# alerts/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from .models import Alert
from .serializers import AlertSerializer

class CreateAlertView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # enable file upload

    def post(self, request, *args, **kwargs):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(f"✅ Alert Received: {serializer.data.get('summary')}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # This will show you the error in the console
        print(f"❌ Invalid data received: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlertSummariesView(APIView):
    def get(self, request, *args, **kwargs):
        alerts = (
            Alert.objects.exclude(summary__isnull=True)
            .exclude(summary="")
            .order_by("-timestamp")[:10]  # last 10
        )
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)