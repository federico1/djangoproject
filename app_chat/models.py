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