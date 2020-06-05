from django.db import models
from django.conf import settings
from courses.models import Course

class Conversation(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                              related_name='conversations_created',
                              on_delete=models.CASCADE)
    course = models.ForeignKey(Course, blank=True, null=True,
                              related_name='course_conversations',
                              on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=0)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class ConversationMember(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='conversation_member',
                              on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, blank=True, null=True,
                              related_name='conversation_members',
                              on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=0)

    class Meta:
        ordering = ['conversation']

    def __str__(self):
        return self.conversation

class Message(models.Model):
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    sent = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='messages_sent',
                              on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, blank=True, null=True,
                              related_name='conversation_messages',
                              on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=0)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.content

class VideoRoom(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField(null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,
                              related_name='rooms_created',
                              on_delete=models.CASCADE)
    course = models.ForeignKey(Course, blank=True, null=True,
                              related_name='course_rooms',
                              on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20)
    participant_count = models.IntegerField(default=0, null=True, blank=True)
    participant_max = models.IntegerField(default=2, null=True, blank=True)
    start_date = models.DateTimeField(blank=True, null=True)
    start_time = models.TextField(blank=True, null=True)

    is_deleted = models.BooleanField(default=0)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

class VideoParticipant(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    member = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='video_room_member',
                              on_delete=models.CASCADE)
    room = models.ForeignKey(VideoRoom, blank=True, null=True,
                              related_name='participants',
                              on_delete=models.CASCADE)

    is_deleted = models.BooleanField(default=0)

    class Meta:
        ordering = ['room']

    def __str__(self):
        return self.room

class VideoRoomLog(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='video_log_owner',
                              on_delete=models.CASCADE)
    room = models.ForeignKey(VideoRoom, blank=True, null=True,
                              related_name='logs',
                              on_delete=models.CASCADE)

    status = models.TextField(blank=True, null=True)
    api_info = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['room']

    def __str__(self):
        return self.room