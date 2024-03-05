from django.urls import path
from . import views
#from django.conf import settings

urlpatterns = [
    path('dashboard/',
         views.HomeView.as_view(),
         name='business_dashboard'),
]
