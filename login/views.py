from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class AddDataAPIView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('files')
            file_details = []
            for file in files:
                # Collect file details
                file_details.append({
                    'filename': file.name,
                    'size': file.size,
                    'content_type': file.content_type,
                })

            return Response({"message": "files generate successfully", "files": file_details}, status=status.HTTP_201_CREATED)
        except Exception as _error:
            return Response({"error": str(_error)}, status=status.HTTP_400_BAD_REQUEST)
       