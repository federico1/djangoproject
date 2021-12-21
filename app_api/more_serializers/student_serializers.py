from rest_framework import serializers
from students.models import User, SSTCard
from app_api.serializers import UserSerializer
from .course_serializers import EnrollmentP2Serializer
from .quiz_serializers import TakenQuizSerializer, StudentAnswerSerializer


class SSTCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSTCard
        fields = ['card_id', 'card_type', 'qr_code',
                  'renew_status', 'issued', 'expired']

    def to_representation(self, instance):
        self.fields['student'] = UserSerializer(read_only=True)
        return super(SSTCardSerializer, self).to_representation(instance)


class StudentHistorySerializer(serializers.ModelSerializer):

    course_enrolled = EnrollmentP2Serializer(read_only=True, many=True)
    taken_quizzes = TakenQuizSerializer(read_only=True, many=True)
    quiz_answers = StudentAnswerSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'course_enrolled', 'taken_quizzes', 'quiz_answers')

    def to_representation(self, instance):
        return super(StudentHistorySerializer, self).to_representation(instance)
