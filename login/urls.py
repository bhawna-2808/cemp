from django.contrib import admin
from django.urls import path, include

from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('api/add_document/', AddDocumentAPIView.as_view(), name='file-upload'),
    path('api/view_files/', file_list_view, name='file-list'),
    path('api/edit/<str:file_name>/', EditDocumentView.as_view(), name='edit-file'),

   
   
]
