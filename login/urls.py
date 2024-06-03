from django.contrib import admin
from django.urls import path, include

from .views import *


urlpatterns = [
    path('add_document/', AddDocumentAPIView.as_view(), name='file-upload'),
    path('view_files/', file_list_view, name='file-list'),
    path('edit/<str:file_name>/', EditDocumentView.as_view(), name='edit-file'),

]
