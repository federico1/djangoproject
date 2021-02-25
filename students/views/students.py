import datetime
import itertools
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.db import transaction
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from students.forms import CourseEnrollForm
from students.forms import StudentSignupForm

from students.forms import TakeQuizForm
from courses.models import Course
from students.models import Quiz
from students.models import Student
from students.models import TakenQuiz
from students.models import User
from courses.models import Review
from courses.models import Cluster
from courses.models import CourseProgress
from courses.models import Content as ModuleContent
from django.core.mail import mail_admins
from django.contrib import messages
from students.decorators import student_required

from courses.suggestions import update_clusters
from students.file_utils import uploaded_file


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()

        qs = qs.filter(students__in=[self.request.user])
        return qs


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    # def get_queryset(self):

    #     qs = super(StudentCourseDetailView, self).get_queryset()

    #     print(qs)

    #     qs = qs.filter(students__in=[self.request.user])

    #     print(qs)

    #     return qs

    def get_context_data(self, **kwargs):

        context = super(StudentCourseDetailView,
                        self).get_context_data(**kwargs)

        course = self.get_object()

        context['prev_completed'] = True
        context['module'] = None
        context['completed_contents'] = []
        context['taken_quizzes'] = []
        context['active_content'] = None
        context['next_content'] = None
        context['content_completed'] = True

        course_details = []
        modules_list = course.modules.all().order_by('order')

        student = self.request.user.student

        taken_quizzes = list(
            student.taken_quizzes.values_list('quiz_id', flat=True))

        for m in modules_list:

            for c in m.contents.order_by('order'):

                c_count = CourseProgress.objects.filter(
                    content_id=c.id, is_completed=True, user=self.request.user).count()

                item_obj = {'type': 'content', 'object': c, 'module': m,
                            'complete': True if c_count > 0 else False}

                course_details.append(item_obj)

                if c_count <= 0:
                    context['content_completed'] = False

            if m.quiz is not None:
                
                if m.quiz.questions.count() > 0:
                    
                    t_q = student.taken_quizzes.filter(
                    quiz_id=m.quiz.id).select_related('quiz').first()

                    score = 0

                    if t_q is not None:
                        score = t_q.score

                    item_obj = {'type': 'quiz',
                                'object': m.quiz, 'score': score, 'module': m, 'complete': True if m.quiz.id in taken_quizzes else False}

                    course_details.append(item_obj)

        context['taken_quizzes'] = taken_quizzes
        context['active_content'] = course_details[0]
        context['completed_contents'] = [x['object'].id for
                                         x in course_details if x['complete'] == True and x['type'] == 'content']

        if 'module_id' in self.kwargs and self.request.GET.get('content'):

            content_id = int(self.request.GET.get('content'))
            context['module'] = course.modules.get(id=self.kwargs['module_id'])

            if self.request.GET.get('type') == 'quiz':
                context['active_content'] = [x for
                                             x in course_details if x['object'].id == content_id and x['type'] == 'quiz'][0]
            else:
                context['active_content'] = [x for
                                             x in course_details if x['object'].id == content_id and x['type'] == 'content'][0]

            if self.request.GET.get('type') == 'quiz':
                current_index = [ix for ix, x in enumerate(
                    course_details) if x['object'].id == content_id and x['type'] == 'quiz'][0]
            else:
                current_index = [ix for ix, x in enumerate(
                    course_details) if x['object'].id == content_id and x['type'] == 'content'][0]

            if current_index > 0:
                prev_item = course_details[current_index-1]
                context['prev_completed'] = prev_item['complete']

            i = current_index+1

            while i < len(course_details):
                obj = course_details[i]
                context['next_content'] = obj
                break
        elif self.request.GET.get('type') == 'quiz' and course.quiz is not None:
            t_q = student.taken_quizzes.filter(
                quiz_id=course.quiz_id).select_related('quiz').first()
            score = 0

            if t_q is not None:
                score = t_q.score

            context['active_content'] = {'type': 'quiz',
                                         'object': course.quiz, 'score': score, 'module': None, 'complete': True if course.quiz.id in taken_quizzes else False}

        return context

    def render_to_response(self, context, **response_kwargs):

        if context['module'] and (context['prev_completed'] == False or context['active_content'] == None):
            return redirect('student_course_detail', self.get_object().id)

        # if self.request.GET.get('content') and context['active_content'] is not None:
        #     try:
        #         pr_r = CourseProgress.objects.update_or_create(content_id=context['active_content']['object'].id,
        #                                                        user=self.request.user, defaults={'user': self.request.user, 'content': context['active_content']['object'], 'is_completed': True})

        #         if context['active_content'] is not None and pr_r[1] == True:
        #             context['active_content']['complete'] = True

        #     except Exception as ex:
        #         print(ex)

        return super(StudentCourseDetailView, self).render_to_response(context, **response_kwargs)

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class StudentRegistrationView(CreateView):
    model = User
    template_name = 'registration/signup_form.html'
    form_class = StudentSignupForm
    success_url = reverse_lazy('student_course_list')

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):

        result = super(StudentRegistrationView, self).form_valid(form)

        cd = form.cleaned_data

        user = authenticate(username=cd['username'], password=cd['password1'])

        mail_admins("A new student user is sign up",
                    "check email on myelearning")
        login(self.request, user)

        return result


class StudentEnrollCourseView(FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name',)
    context_object_name = 'quizzes'
    template_name = 'students/student/quiz_list.html'

    def get_queryset(self):
        try:
            student = self.request.user.student
            student_interests = student.interests.values_list('pk', flat=True)
            taken_quizzes = student.quizzes.values_list('pk', flat=True)
            queryset = Quiz.objects.filter(tags__in=student_interests).exclude(
                pk__in=taken_quizzes).annotate(question_count=Count('questions')).filter(question_count__gt=0)
            return queryset
        except ObjectDoesNotExist:
            return self.request.user


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'students/student/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes.select_related(
            'quiz', 'quiz__tags').order_by('quiz__name')

        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():

        if request.GET['ref'] is not None:
            return redirect(request.GET['ref'] + "&type=quiz")

        return redirect('taken_quiz_list')

    total_questions = quiz.questions.count()
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

                rev_url = reverse('take_quiz', kwargs={"pk": pk})

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

    return render(request, 'students/student/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': (total_questions - total_unanswered_questions) + 1,
        'total_questions': total_questions
    })


@login_required
@student_required
def quiz_result(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)

    student = request.user.student

    taken = student.taken_quizzes.filter(quiz=pk).last()

    if taken.score < 50.0:
        messages.warning(request, 'Good luck for next time! Your score for this quiz %s was %s.' % (
            quiz.name, taken.score))
    else:
        messages.success(request, 'Fantastic! You completed the quiz %s with success! Your scored %s points.' % (
            quiz.name, taken.score))

    return render(request, 'students/student/quiz_result.html', {
        'quiz': quiz,
    })


@login_required
def student_recommendation_list(request):
    user_reviews = Review.objects.filter(
        user_name=request.user).prefetch_related('course')
    user_review_course_ids = set(map(lambda x: x.course.id, user_reviews))

    try:
        user_cluster_name = User.objects.get(
            username=request.user.username).cluster_set.first().name
    except:
        update_clusters()
        user_cluster_name = User.objects.get(
            username=request.user.username).cluster_set.first().name

    user_cluster_other_members = Cluster.objects.get(
        name=user_cluster_name).users.exclude(username=request.user.username).all()
    others_members_usernames = set(
        map(lambda x: x, user_cluster_other_members))

    others_users_reviews = Review.objects.filter(
        user_name__in=others_members_usernames).exclude(course__id__in=user_review_course_ids)
    others_users_reviews_courses_ids = set(
        map(lambda x: x.course.id, others_users_reviews))

    course_list = sorted(
        list(Course.objects.filter(id__in=others_users_reviews_courses_ids)),
        key=lambda x: x.average_rating(),
        reverse=True
    )
    return render(request, 'students/reviews/student_recommendation_list.html', {'student': request.user.username, 'course_list': course_list})


@login_required
@student_required
def quiz_reset(request, pk):
    try:
        student = request.user.student
        taken = student.taken_quizzes.filter(quiz=pk).last()
        quiz = Quiz.objects.get(id=pk)

        rev_url = reverse('take_quiz', kwargs={"pk": pk})

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


@login_required
@student_required
def quick_course_enrol(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if course:
        enrolled = request.user.courses_joined.filter(id=course.id).count()
        if enrolled > 0:
            rev_url = reverse('student_course_detail', args=[course.id])
            return redirect(rev_url)

        rev_url = reverse('course_detail', args=[course.slug])
        return redirect(rev_url)


def file_upload(request):

    result = 0

    if request.method == 'POST' and request.FILES['file']:
        result = uploaded_file(request.FILES['file'])

    return HttpResponse(result)


class StudentCourseDetailView2(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail2.html'

    def get_queryset(self):

        qs = super(StudentCourseDetailView2, self).get_queryset()
        qs = qs.filter(students__in=[self.request.user])

        return qs

    def get_context_data(self, **kwargs):

        context = super(StudentCourseDetailView2,
                        self).get_context_data(**kwargs)

        course = self.get_object()

        return context

    def render_to_response(self, context, **response_kwargs):
        return super(StudentCourseDetailView2, self).render_to_response(context, **response_kwargs)

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
