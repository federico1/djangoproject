from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db import transaction
from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin, View

from students.decorators import student_required
from students.forms import TakeQuizForm
from students.models import Quiz, TakenQuiz


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    student = request.user

    if student.taken_quizzes.filter(quiz=pk).exists():

        if request.GET['ref'] is not None:
            return redirect(request.GET['ref'] + "&type=quiz")

        return redirect('student_taken_quiz_list')

    total_questions = quiz.questions.count()

    if total_questions <= 0:
        return redirect('student_taken_quiz_list')

    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()

    progress = 100 - \
        round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)

        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                unanswered_questions = student.get_unanswered_questions(quiz)
                total_unanswered_questions = unanswered_questions.count()

                rev_url = reverse('student_take_quiz', kwargs={"pk": pk})

                if request.GET['ref'] is not None:
                    rev_url = rev_url + "?ref=" + \
                        request.GET['ref'] + '&type=quiz'

                request.user.save()

                if unanswered_questions.exists():
                    return redirect(rev_url)
                else:
                    correct_answers = student.quiz_answers.filter(
                        answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round(
                        (correct_answers / total_questions) * 100.0, 2)

                    TakenQuiz.objects.create(
                        student=student, quiz=quiz, score=score)

                    return redirect(rev_url)
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'quiz/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': (total_questions - total_unanswered_questions) + 1,
        'total_questions': total_questions
    })


@login_required
@student_required
def quiz_reset(request, pk):
    try:
        student = request.user
        taken = student.taken_quizzes.filter(quiz=pk).last()
        quiz = Quiz.objects.get(id=pk)

        rev_url = reverse('student_take_quiz', kwargs={"pk": pk})

        if request.GET['ref'] is not None:
            rev_url = rev_url + "?ref=" + request.GET['ref']

        if taken:
            answers = [x for x in quiz.questions.select_related(
                'answers').values_list('answers', flat=True)]

            for item in student.quiz_answers.filter(answer_id__in=answers):
                item.delete()

            taken.delete()
            return redirect(rev_url)
        else:
            return HttpResponse(0)
    except Exception as ex:
        return HttpResponse(0)


class TakenQuizTemplateView(TemplateResponseMixin, View):
    template_name = 'quiz/taken_list.html'

    def get(self, request):
        return self.render_to_response({})
