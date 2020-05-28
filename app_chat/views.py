from django.shortcuts import render, reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from braces.views import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.http import JsonResponse, HttpResponse

from .models import Conversation, VideoRoom

from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

from twilio.rest import Client

import json


@method_decorator([login_required], name='dispatch')
class MessagesView(TemplateView):
    template_name = "messages.html"
    
    def get_context_data(self, **kwargs):
       context = super(MessagesView, self).get_context_data(**kwargs)
       context['conversation'] = None

       if 'pk' in self.kwargs:
           context['conversation'] = Conversation.objects.get(pk=self.kwargs['pk'])
       return context

@method_decorator([login_required], name='dispatch')
class VideoRoomsView(TemplateView):
    template_name = "video_rooms.html"
    
    def get_context_data(self, **kwargs):
       context = super(VideoRoomsView, self).get_context_data(**kwargs)
       return context

class VideoRoomDetailView(DetailView):
    model = VideoRoom
    template_name = 'video_room_detail.html'

    def get_context_data(self, **kwargs):
        context = super(VideoRoomDetailView,
                        self).get_context_data(**kwargs)
        return context

@login_required
def create_room(request):


    room_obj = VideoRoom.objects.get(id=request.GET.get('id'))
    
    client = Client(twilio_account_sid, t_auth_key)

    room = None

    rooms = client.video.rooms.list(unique_name=room_obj.title, limit=1)
    
    for record in rooms:
        room = record

    if room is None:
        rev_url = request.build_absolute_uri(reverse('video_rooms', kwargs={"pk":room_obj.id}))
    try:
        room = client.video.rooms.create(
                              record_participants_on_connect=True,
                              status_callback=rev_url,
                              type='group',
                              unique_name=room_obj.title
                          )
    except Exception as ex:
        print(ex)

    if room is not None:
        room = {
            'sid': room.sid,
            'type':room.type,
            'status':room.status,
            'unique_name':room.unique_name,
            'duration':room.duration,
            'end_time': room.end_time,
            'url': room.url,
            'links': room.links
        }

        room_obj.info = json.dumps(room)
        room_obj.save()

    return JsonResponse(room, safe=False)

@login_required
def complete_room(request):

    client = Client(twilio_account_sid, t_auth_key)

    room_obj = VideoRoom.objects.get(id=request.GET.get('id'))

    rooms = client.video.rooms.list(unique_name=room_obj.title, limit=1)
    
    room=None

    for record in rooms:
        room = record.update(status='completed')


    if room is not None:
        room = {
            'sid': room.sid,
            'type':room.type,
            'status':room.status,
            'unique_name':room.unique_name,
            'duration':room.duration,
            'end_time': room.end_time,
            'url': room.url,
            'links': room.links
        }

    return JsonResponse(room, safe=False)


@login_required
def create_video_token(request):

    if request.method == 'POST':
        data = json.loads(request.body)

        client = Client(twilio_account_sid, t_auth_key)

        token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=request.user.username)
        
        room = client.video.rooms(str(data['room_sid'])).fetch()
        
        token.add_grant(VideoGrant(room=room.sid))
        
        d = {'token': token.to_jwt().decode()}
        
        return JsonResponse(d)
