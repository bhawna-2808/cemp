<<<<<<< HEAD
=======

>>>>>>> 65dca7953e43a17f9490db0bf4813ef2cca0c3df
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
<<<<<<< HEAD
# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
=======
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

>>>>>>> 65dca7953e43a17f9490db0bf4813ef2cca0c3df


class AddDocumentAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('files')
            file_details = []

            upload_dir = os.path.join(settings.BASE_DIR, 'uploaded_files')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
                logger.info(f"Created directory: {upload_dir}")

            for file in files:
                file_path = os.path.join(upload_dir, file.name)
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                logger.info(f"Saved file to: {file_path}")

                if not os.path.exists(file_path):
                    logger.error(f"File not found after saving: {file_path}")
                    continue

                file_url = request.build_absolute_uri(settings.MEDIA_URL + 'uploaded_files/' + file.name)

                text = ""
                if file.content_type == 'application/pdf':
                    text = self.extract_text_from_pdf(file_path)
                    # entities =  extract_entities_ner(text)
                    # print(entities)
                    facility_name = extract_facility_name(text)
                    print("Facility Name:", facility_name)
    
    
                
                elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    text = self.extract_text_from_docx(file_path)
                elif file.content_type == 'application/msword':
                    text = self.extract_text_from_doc(file_path)
                elif file.content_type.startswith('image/'):
                    text = self.extract_text_from_image(file_path)
                else:
                    text = 'Unsupported file type for text extraction.'

                text_html = self.format_text_to_html_paragraphs(text)

                file_details.append({
                    'filename': file.name,
                    'size': file.size,
                    'content_type': file.content_type,
                    'path': file_path,
                    'url': file_url,
                    'text': text_html,
                })

            file_list_url = request.build_absolute_uri(reverse('file-list'))
            return Response({"message": "Files uploaded successfully", "files": file_details, "file_list_url": file_list_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def extract_text_from_pdf(self, file_path):
        try:
            text = ""
            logger.info(f"Extracting text from PDF file: {file_path}")

            pdf_document = fitz.open(file_path)

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                page_text = page.get_text()

                image_list = page.get_images(full=True)
                for img in image_list:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    image_text = pytesseract.image_to_string(image)
                    page_text += image_text.strip() + '\n'

                text += page_text.strip() + '\n'
                logger.info(f"Processed page {page_num + 1} of {len(pdf_document)}")

            logger.info("Text extraction from PDF successful.")
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return f'Error extracting text from PDF: {str(e)}', []

    def extract_text_from_doc(self, file_path):
        try:
            logger.info(f"Extracting text from DOC file: {file_path}")

            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return f'File not found: {file_path}', []

            # Use antiword for text extraction
            result = subprocess.run(['antiword', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            if result.returncode != 0:
                logger.error(f"Error extracting text from DOC: {result.stderr}")
                return f'Error extracting text from DOC: {result.stderr}', []

            text = result.stdout
            logger.info("Text extraction from DOC successful.")
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOC: {str(e)}")
            return f'Error extracting text from DOC: {str(e)}', []


    def extract_text_from_docx(self, file_path):
        try:
<<<<<<< HEAD
=======
            
>>>>>>> 65dca7953e43a17f9490db0bf4813ef2cca0c3df
            logger.info(f"Extracting text from DOCX file: {file_path}")

            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return f'File not found: {file_path}', []

            doc = Document(file_path)
            text = "\n".join(para.text for para in doc.paragraphs)
            logger.info("Text extraction from DOCX successful.")
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from DOCX: {str(e)}")
            return f'Error extracting text from DOCX: {str(e)}', []

    def extract_text_from_image(self, file_path, config='--psm 6',grayscale=True):
        try:
            logger.info(f"Extracting text from image file: {file_path}")

            img = Image.open(file_path)
             # Preprocessing (adjust based on image characteristics)
            if grayscale:
                img = img.convert('L')  # Convert to grayscale

            # Logging for debugging
            logger.info(f"Image shape after grayscale conversion: {img.size}")
            logger.info(f"Image data type after grayscale conversion: {img.mode}")
                # Noise reduction (example)
            # Apply a median filter to reduce noise
            img = cv2.medianBlur(np.array(img), 3)
            # Binarization (example)
            # Convert to binary image for better text extraction
            thresh = cv2.threshold(np.array(img), 127, 255, cv2.THRESH_BINARY)[1]

            #  Optional: Additional preprocessing steps like skew correction or layout analysis

            # Text extraction with Tesseract
            text = pytesseract.image_to_string(thresh, config=config)
            # text = pytesseract.image_to_string(img)
<<<<<<< HEAD
            
=======

>>>>>>> 65dca7953e43a17f9490db0bf4813ef2cca0c3df
            logger.info("Text extraction from image successful.")
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from image: {str(e)}")
            return f'Error extracting text from image: {str(e)}', []

    def format_text_to_html_paragraphs(self, text):
        if isinstance(text, str):
            paragraphs = text.split('\n\n')
            formatted_text = ''.join('<p>{}</p>'.format(paragraph.replace("\n", "<br>")) for paragraph in paragraphs)
            return formatted_text
        else:
            return 'Invalid text format.'

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
<<<<<<< HEAD
=======

>>>>>>> 65dca7953e43a17f9490db0bf4813ef2cca0c3df
