from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.utils import timezone


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_business = models.BooleanField(default=False)
    cell_number = models.CharField(max_length=20, null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    designation = models.TextField(null=True, blank=True)
    company_name = models.TextField(null=True, blank=True)
    personal_id = models.TextField(null=True, blank=True)
    company_id = models.TextField(null=True, blank=True)

    @property
    def full_name(self):
        return self.first_name+" "+self.last_name
        
    def get_unanswered_questions(self, quiz):

        answered_questions = self.quiz_answers \
            .filter(answer__question__quiz=quiz) \
            .values_list('answer__question__pk', flat=True)
        
        questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')

        return questions


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username


class Tag(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#007bff')

    def __str__(self):
        return self.name

    def get_html_badge(self):
        name = escape(self.name)
        color = escape(self.color)
        html = '<span class="badge badge-primary" style="background-color: %s">%s</span>' % (
            color, name)
        return mark_safe(html)


class Quiz(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='quizzes')
    tags = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name='quizzes')

    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField('Question', max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField('Answer', max_length=255)
    is_correct = models.BooleanField('Correct answer', default=False)

    def __str__(self):
        return self.text


class TakenQuiz(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='taken_quizzes')
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name='taken_quizzes')
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}. {} {}%'.format(self.quiz, self.student, self.score)


class StudentAnswer(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='quiz_answers')
    answer = models.ForeignKey(
        Answer, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return '{} {}'.format(self.student, self.answer)

class SSTCard(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sst_cards')
    card_id = models.TextField()
    card_type = models.TextField(null=True, blank=True)
    qr_code = models.TextField(null=True, blank=True)
    renew_status = models.TextField(null=True, blank=True)
    issued = models.DateTimeField(auto_now_add=True)
    expired = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.card_id)