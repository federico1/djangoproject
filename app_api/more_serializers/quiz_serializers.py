from rest_framework import serializers
from students.models import TakenQuiz, Quiz, Question, Answer, StudentAnswer
from app_api.serializers import UserSerializer


class TakenQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = TakenQuiz
        fields = ('id', 'quiz', 'score', 'date')


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = '__all__'

    def to_representation(self, instance):
        return super(StudentAnswerSerializer, self).to_representation(instance)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

    def to_representation(self, instance):
        return super(AnswerSerializer, self).to_representation(instance)


class QuestionSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'quiz', 'text', 'answers')

    def to_representation(self, instance):
        return super(QuestionSerializer, self).to_representation(instance)


class QuizSerializer(serializers.ModelSerializer):

    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ('id', 'name', 'owner', 'tags', 'questions')

    def to_representation(self, instance):
        return super(QuizSerializer, self).to_representation(instance)


class QuizCoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quiz
        fields = ('id', 'name', 'owner', 'tags')

    def to_representation(self, instance):
        return super(QuizCoreSerializer, self).to_representation(instance)

