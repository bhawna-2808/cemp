
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
from io import BytesIO
from PyPDF2 import PdfReader  # Import PdfReader instead of PdfFileReader

# Set up logging
logger = logging.getLogger(__name__)
# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract' 


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
                text1 = self.format_text_to_html_paragraphs(text)    
                # text.replace('\n', '<br>')
                file_details.append({
                    'filename': file.name,
                    'size': file.size,
                    'content_type': file.content_type,
                    'path': file_path,
                    'url': file_url,
                    'text': text1
                })

            file_list_url = request.build_absolute_uri(reverse('file-list'))
            return Response({"message": "Files uploaded successfully", "files": file_details, "file_list_url": file_list_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(e)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def extract_text_from_pdf(self,file_path):
        try:
            text = ""
            logger.info(f"Extracting text from PDF file: {file_path}")
            
            # Open the PDF file using PyMuPDF
            pdf_document = fitz.open(file_path)
            
            # Iterate over each page
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
                    text += image_text.strip() + '\n'
                
                # Append page text to the result
                text += page_text.strip() + '\n'
                
                # Log progress
                logger.info(f"Processed page {page_num + 1} of {len(pdf_document)}")
            
            logger.info("Text extraction from PDF successful.")
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {str(e)}")
            return f'Error extracting text from PDF: {str(e)}'

    def format_text_to_html_paragraphs(self,text):
        """
        This function takes a string with newline characters and replaces them with HTML tags for paragraphs and line breaks.
        
        Parameters:
        text (str): The input string with newline characters.
        
        Returns:
        str: The formatted string with HTML tags.
        """
        # Split the text by double newline characters to separate paragraphs
        paragraphs = text.split('\n\n')
        # Wrap each paragraph in <p> tags and replace single newlines with <br>
        formatted_text = ''.join('<p>{}</p>'.format(paragraph.replace("\n", "<br>")) for paragraph in paragraphs)

        # formatted_text = ''.join(f'<p>{paragraph.replace("\n", "<br>")}</p>' for paragraph in paragraphs)
    # 
        return formatted_text
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
