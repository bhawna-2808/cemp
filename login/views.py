import os
import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from docx import Document

# pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
# pytesseract.pytesseract.tesseract_cmd = '/user/bin/tesseract'




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
                # Define the file path
                file_path = os.path.join(upload_dir, file.name)

                # Save the file to the directory
                path = default_storage.save(file_path, ContentFile(file.read()))

                # Generate the URL for the saved file
                file_url = request.build_absolute_uri(settings.MEDIA_URL + 'uploaded_files/' + file.name)
                
                # Extract text based on file type
                text = ""
                if file.content_type == 'application/pdf':
                    # Extract text from PDF
                    text = self.extract_text_from_pdf(file)
                elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                    # Extract text from DOCX
                    text = self.extract_text_from_docx(file)
                elif file.content_type.startswith('image/'):
                    # Extract text from image
                    text = self.extract_text_from_image(file)    
                else:
                    text = 'Unsupported file type for text extraction.'

                # Collect file details
                file_details.append({
                    'filename': file.name,
                    'size': file.size,
                    'content_type': file.content_type,
                    'path': path,
                    'url': file_url,
                    'text': text
                })

            # Generate the URL for the file list view
            file_list_url = request.build_absolute_uri(reverse('file-list'))
            return Response({"message": "Files generated successfully", "files": file_details, "file_list_url": file_list_url}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def extract_text_from_pdf(self, file):
        try:
            # Use PyMuPDF to extract text and images
            file.seek(0)  # Reset file pointer to the beginning
            pdf_document = fitz.open(stream=file.read(), filetype="pdf")
            text = ""

            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                page_text = page.get_text()

                # Extract images from the page
                image_list = page.get_images(full=True)
                
                for img in image_list:
                    xref = img[0]
                    base_image = pdf_document.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))

                    # Use OCR to extract text from images
                    image_text = pytesseract.image_to_string(image)
                    text += image_text + '\n\n'  # Append image text to the page text

                text += page_text.strip() + '\n\n'  # Append page text to overall text

            return text.strip()
        except Exception as e:
            return f'Error extracting text from PDF: {str(e)}'

    def extract_text_from_docx(self, file):
        try:
            # Extract text from DOCX
            text = ""
            doc = Document(file)
            for para in doc.paragraphs:
                text += para.text + '\n'
            return text.strip()
        except Exception as e:
            return f'Error extracting text from DOCX: {str(e)}'
    
    def extract_text_from_image(self, file):
        try:
            # Open the image file
            image = Image.open(file)

            # Use OCR to extract text from the image
            text = pytesseract.image_to_string(image)

            return text.strip()
        except Exception as e:
            return f'Error extracting text from image: {str(e)}'    
    
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