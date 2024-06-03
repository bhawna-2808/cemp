import os
from django.conf import settings


def load_document(file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploaded_files', file_name)
    with open(file_path, 'rb') as file:
        document = file.read()
    return document


def preprocess_document(document):
    # Implement preprocessing tasks here
    # For example, you can clean up the document, remove unwanted characters,
    # or transform the data as needed
    
    # For demonstration purposes, let's assume we want to convert the document content to lowercase
    preprocessed_document = document.lower()
    
    return preprocessed_document