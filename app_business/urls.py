from django.urls import path
from .views import dashboard_views, public_views


urlpatterns = [
    path('dashboard/',
         dashboard_views.HomeView.as_view(),
         name='business_dashboard'),
     path('account-register/', public_views.RegisterBusinessUserView.as_view(),
         name='business_user_register'),
]

