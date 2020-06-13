from django.urls import path, include
from .views import MessagesView, VideoRoomsView, VideoRoomDetailView, create_video_token, create_room, complete_room, AllVideoRoomsView
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('messages/', MessagesView.as_view(), name='messages'),
    path('messages/<int:pk>/', MessagesView.as_view(), name='messages'),

    path('video-rooms/', VideoRoomsView.as_view(), name='video_rooms'),
    path('video-rooms/<int:pk>/', VideoRoomDetailView.as_view(), name='video_rooms'),

    path('video-token/', create_video_token, name='video-token'),
    path('create-room/', create_room, name='create-room'),
    path('complete-room/', complete_room, name='complete-room'),

    path('live-classes/', AllVideoRoomsView.as_view(), name='live_classes'),

]
