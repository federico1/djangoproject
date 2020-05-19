from django.urls import path, include
from .views import MessagesView
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('messages/', MessagesView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessagesView.as_view(), name='messages'),
]
