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
from rest_framework.views import APIView
from login.ai import *
import pytesseract
from PIL import Image
from PyPDF2 import PdfFileReader
from docx import Document


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
                
                # Generate the URL for editing the file
                edit_url = request.build_absolute_uri(reverse('edit-file', kwargs={'file_name': file.name}))
                
                # Extract text based on file type
                text = ""
                if file.content_type == 'application/pdf':
                    # Extract text from PDF
                    reader = PdfFileReader(file)
                    for page_num in range(reader.numPages):
                        text += reader.getPage(page_num).extract_text()
                elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    # Extract text from DOCX
                    doc = Document(file)
                    for para in doc.paragraphs:
                        text += para.text + '\n'
                elif file.content_type.startswith('image/'):
                    # Extract text from image using OCR
                    image = Image.open(file)
                    text = pytesseract.image_to_string(image)
                    # Clean up the extracted text
                    text = text.replace('\n', ' ').replace('\r', '').strip()
                else:
                    text = 'Unsupported file type for text extraction.'

                # Collect file details
                file_details.append({
                    'filename': file.name,
                    'size': file.size,
                    'content_type': file.content_type,
                    'path': path,
                    'url': file_url,
                    'edit_url': edit_url,
                    'text': text
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



class EditDocumentView(APIView):
    def get(self, request, file_name, *args, **kwargs):
        try:
            # Load the document (e.g., DOCX)
            document, type_of_file = load_document(file_name)
            print(document)
            print(type_of_file)
            return Response({"message": "Document edited successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




def home(request):
    return render(request, 'home.html')