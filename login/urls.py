from django.contrib import admin
from django.urls import path, include

from .views import *


urlpatterns = [
    path('add_document/', AddDocumentAPIView.as_view(), name='file-upload'),
    path('view_files/', file_list_view, name='file-list'),
]
