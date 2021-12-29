from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import api_view

from django.http import Http404
from django.db.models import Count

from app_chat.models import ExternalVideoRoom, Conversation, ConversationMember, Message
from app_api.more_serializers.chat_serializers import ExternalVideoRoomSerializer, \
    ConversationSerializer, ConversationMemberSerializer, MessageSerializer

from students.models import User
from django.conf import settings

from django.utils.timezone import localtime, now


class ExternalVideoRoomDetailView(APIView):

    def get_object(self, pk):
        try:
            return ExternalVideoRoom.objects.get(pk=pk)
        except ExternalVideoRoom.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        course_id = request.query_params.get('course')
        today = request.query_params.get('today')
        is_delete = request.query_params.get('delete')

        snippets = ExternalVideoRoom.objects.filter(course_id=course_id)

        if today:
            snippets = snippets.filter(
                created__startswith=localtime(now()).date())

        if is_delete:
            is_delete = True if is_delete == 'true' else False

            snippets = snippets.filter(is_deleted=is_delete)

        serializer = ExternalVideoRoomSerializer(snippets, many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ExternalVideoRoomSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.is_deleted = True
        snippet.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ConversationDetailView(APIView):

    def get_object(self, pk):
        try:
            return Conversation.objects.get(pk=pk)
        except Conversation.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        snippets = Conversation.objects

        # if request.user.is_student == True:
        #     c_list = \
        #         request.user.conversation_member.values_list(
        #             'conversation_id', flat=True)
        #     snippets = Conversation.objects.filter(id__in=c_list)

        serializer = ConversationSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConversationSerializer(data=request.data)

        if serializer.is_valid():

            if request.user.is_student == True:
                data = serializer.validated_data
                conversation = Conversation.objects.filter(course=data['course'],
                                                           conversation_members__member__in=[request.user.id, request.data['teacher']])
                print(conversation.count)
                if conversation.count() > 0:
                    serializer = ConversationSerializer(conversation, many=True)

                    return Response(serializer.data[0], status=status.HTTP_201_CREATED)
                else:
                    serializer.save()
                    ConversationMember.objects.bulk_create(
                        [ConversationMember(member_id=request.user.id, conversation_id=serializer.data['id']),
                         ConversationMember(member_id=request.data['teacher'], conversation_id=serializer.data['id'])])

                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ConversationMembersList(APIView):

    def get_object(self, pk):
        try:
            return ConversationMember.objects.get(pk=pk)
        except ConversationMember.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        c_id = request.query_params.get('conversation')
        snippets = \
            ConversationMember.objects.filter(conversation_id=c_id)
        serializer = ConversationMemberSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ConversationMemberSerializer(data=request.data)
        if serializer.is_valid():
            a_count = \
                ConversationMember.objects.filter(conversation_id=int(request.data['conversation'
                                                                                   ]), member_id=int(request.data['member'])).count()

            if a_count <= 0:
                serializer.save()

            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(
        self,
        request,
        pk,
        format=None,
    ):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageList(APIView):

    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            raise Http404

    def get(self, request, format=None):

        c_id = request.query_params.get('conversation')
        type = request.query_params.get('type')

        snippets = Message.objects.filter(conversation_id=c_id)

        if type is not None or type == 'last10':
            snippets =snippets.order_by('-id')[:10][::-1]

        serializer = MessageSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)