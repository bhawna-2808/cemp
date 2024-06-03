from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from rest_framework import status
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.urls import reverse

class AddDocumentAPIView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('files')
            file_details = []

            # Define the directory where you want to save the files
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_files')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            for file in files:
                # Define the file path
                file_path = os.path.join(upload_dir, file.name)

                # Save the file to the directory
                path = default_storage.save(file_path, ContentFile(file.read()))
                # Generate the URL for the saved file
                file_url = request.build_absolute_uri(settings.MEDIA_URL + 'uploaded_files/' + file.name)
                # Collect file details
                file_details.append({
                    'filename': file.name,
                    'size': file.size,
                    'content_type': file.content_type,
                    'path': path,  # Optional: Return the path where the file is saved,
                    'url':file_url
                    
                })

            # Generate the URL for the file list view
            file_list_url = request.build_absolute_uri(reverse('file-list'))
            return Response({"message": "files generated successfully", "files": file_details, "file_list_url": file_list_url}, status=status.HTTP_201_CREATED)
        except Exception as _error:
            return Response({"error": str(_error)}, status=status.HTTP_400_BAD_REQUEST)


def file_list_view(request):
    # Define the directory where the files are saved
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_files')
    
    # Get list of files in the directory
    files = []
    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        if os.path.isfile(file_path):
            files.append({
                'filename': filename,
                'size': os.path.getsize(file_path),
                'path': file_path
            })

    return JsonResponse({'files': files})
