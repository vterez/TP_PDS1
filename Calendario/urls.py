from django.urls import path
from .views import *

urlpatterns = [
    path('',Inicial,name='Inicial'),
    path('Confirm',Confirm,name='Confirm'),
    path('Upload',Upload,name='Upload'),
    path('Uploaded',Uploaded,name='Uploaded'),
]
