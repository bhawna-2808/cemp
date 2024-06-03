from django.contrib import admin
from django.urls import path, include

from .views import *


urlpatterns = [
    path('add_data/', AddDataAPIView.as_view()),
]
