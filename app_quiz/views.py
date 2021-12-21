from django.views.generic.edit import CreateView
from students.models import Quiz, Question, Answer, Tag
from courses.models import Module, Course
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.db import transaction

from django.http import HttpResponse

from .forms import QuestionForm, BaseAnswerInlineFormSet


def question_add(request, module_id=None):
    module = get_object_or_404(Module, pk=module_id)
    question = Question()

    if request.GET.get('question_id') is not None:
        question_pk = request.GET.get('question_id')
        question = get_object_or_404(
            Question, pk=question_pk, quiz=module.quiz)

    if module.quiz is None:
        quiz_object = Quiz()
        quiz_object.name = module.title
        quiz_object.owner = request.user
        quiz_object.tags = Tag.objects.get(name='module')
        quiz_object.save()

        module.quiz = quiz_object
        module.save()

    question.quiz = module.quiz

    AnswerFormSet = inlineformset_factory(
        Question,
        Answer,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)

        with transaction.atomic():

            if form.is_valid() and formset.is_valid():
                form_saved = form.save()
                formset = AnswerFormSet(request.POST, instance=form_saved)

                if form_saved.pk is not None and formset.is_valid():
                    formset.save()
                    return redirect('app_add_question', module_id)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    questions = Question.objects.filter(quiz=module.quiz.id)

    return render(request, 'question_add_form.html', {
        'module': module,
        'questions': questions,
        'form': form,
        'formset': formset
    })


def question_delete(request, module_id=None):

    if request.GET.get('question_id') is not None:
        question_pk = request.GET.get('question_id')
        Question.objects.filter(id=question_pk).delete()
        Answer.objects.filter(question=question_pk).delete()

    return redirect('app_add_question', module_id)


def quiz_course(request, course_id=None):

    course = get_object_or_404(Course, pk=course_id)
    question = Question()

    if request.GET.get('question_id') is not None:
        question_pk = request.GET.get('question_id')
        question = get_object_or_404(
            Question, pk=question_pk, quiz=course.quiz)

    if course.quiz is None:
        quiz_object = Quiz()
        quiz_object.name = course.title
        quiz_object.owner = request.user
        quiz_object.tags = Tag.objects.get(name='course')
        quiz_object.save()

        course.quiz = quiz_object
        course.save()

    question.quiz = course.quiz

    extra_fields = 2
    if request.GET.get('question_id') is not None:
        extra_fields = 0

    AnswerFormSet = inlineformset_factory(
        Question,
        Answer,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True,
        extra=extra_fields
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)

        with transaction.atomic():

            if form.is_valid() and formset.is_valid():
                form_saved = form.save()
                formset = AnswerFormSet(request.POST, instance=form_saved)

                if form_saved.pk is not None and formset.is_valid():
                    formset.save()
                    return redirect('quiz_course', course_id)

    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    questions = Question.objects.filter(quiz=course.quiz.id)

    return render(request, 'quiz_course.html', {
        'course': course,
        'questions': questions,
        'form': form,
        'formset': formset
    })


def question_delete_generic(request, question_id):
    result = 0

    if question_id is not None:
        question_pk = question_id
        Question.objects.filter(id=question_pk).delete()
        Answer.objects.filter(question=question_pk).delete()
        result = 1

    return HttpResponse(result, content_type='text/plain')


def quiz_questions(request, quiz_id=None):

    question = Question()
    quiz = Quiz.objects.get(pk =quiz_id)

    if request.GET.get('question_id') is not None:
        question_pk = request.GET.get('question_id')
        question = get_object_or_404(
            Question, pk=question_pk, quiz=quiz)

    question.quiz = quiz

    extra_fields = 2

    # if request.GET.get('question_id') is not None:
    #     extra_fields = 0

    AnswerFormSet = inlineformset_factory(
        Question,
        Answer,
        fields=('text', 'is_correct'),
        min_num=2,
        validate_min=True,
        max_num=10,
        validate_max=True,
        extra=extra_fields
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)

        with transaction.atomic():

            if form.is_valid() and formset.is_valid():
                form_saved = form.save()
                formset = AnswerFormSet(request.POST, instance=form_saved)

                if form_saved.pk is not None and formset.is_valid():
                    formset.save()
                    return redirect('quiz_question_manager', quiz_id)

    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    questions = Question.objects.filter(quiz=quiz)

    return render(request, 'quiz_question.html', {
        'quiz': quiz,
        'questions': questions,
        'form': form,
        'formset': formset
    })
