from django.urls import path
from .views import LegalView, AboutView, ContactView


urlpatterns = [
    path('legal/',
         LegalView.as_view(),
         name='legal_detail'),
    path('about/',
         AboutView.as_view(),
         name='about_detail'),
    path('contact/',
         ContactView.as_view(),
         name='contact_detail'),
]
