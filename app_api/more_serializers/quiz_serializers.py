from rest_framework import serializers
from students.models import TakenQuiz
from app_api.serializers import UserSerializer


class TakenQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenQuiz
        fields = ('id','quiz', 'score', 'date')
