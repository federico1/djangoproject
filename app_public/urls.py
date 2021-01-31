from django.urls import path
from .views import *

urlpatterns = [
    path('legal/',
         LegalView.as_view(),
         name='legal_detail'),
]
