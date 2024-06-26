import os
import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from docx import Document
import logging
import cv2
import numpy as np
import subprocess
import spacy
import re
from spacy import displacy
from spacy.matcher import Matcher
from spaczz.matcher import FuzzyMatcher
from login.entity import *

# Set up logging
logger = logging.getLogger(__name__)
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # Update the path based on your server configuration
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract' 

class AddDocumentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('files')
            file_details = []

            # Define the directory where you want to save the files
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_files')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            for file in files:
                # Save the file
                file_path = os.path.join(upload_dir, file.name)
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Generate the URL for the saved file
                file_url = request.build_absolute_uri(settings.MEDIA_URL + 'uploaded_files/' + file.name)

                # Extract text based on file type
                text = ""
                if file.content_type == 'application/pdf':
                    text = self.extract_text_from_pdf(file_path)
                elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    text = self.extract_text_from_docx(file_path)
                elif file.content_type.startswith('image/'):
                    text = self.extract_text_from_image(file_path)
                else:
                    text = 'Unsupported file type for text extraction.'

                file_details.append({
                    'filename': file.name,
                    'size': file.size,
                    'content_type': file.content_type,
                    'path': file_path,
                    'url': file_url,
                    'text': text
                })

            file_list_url = request.build_absolute_uri(reverse('file-list'))
            return Response({"message": "Files uploaded successfully", "files": file_details, "file_list_url": file_list_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def extract_text_from_pdf(self, file_path):
        try:
            pdf_document = fitz.open(file_path)
            text = ""

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                page_text = page.get_text()

                # Extract text from images using OCR
                image_list = page.get_images(full=True)
                for img in image_list:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    image_text = pytesseract.image_to_string(image)
                    text += image_text + '\n\n'

                # Append page text to the result
                text += page_text.strip() + '\n\n'

                # Log progress
                logger.info(f"Processed page {page_num + 1} of {len(pdf_document)}")

            return text.strip()
        except Exception as e:
            logger.error(e)
            return f'Error extracting text from PDF: {str(e)}'

    def extract_text_from_docx(self, file_path):
        try:
            text = ""
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + '\n'
            return text.strip()
        except Exception as e:
            logger.error(e)
            return f'Error extracting text from DOCX: {str(e)}'

<<<<<<< HEAD
=======

>>>>>>> 65dca7953e43a17f9490db0bf4813ef2cca0c3df
    def extract_text_from_image(self, file_path):
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            logger.error(e)
            return f'Error extracting text from image: {str(e)}'

def file_list_view(request):
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploaded_files')
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
