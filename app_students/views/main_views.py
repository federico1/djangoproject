from django.views import generic
from django.views.generic.edit import CreateView
from braces.views import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import get_template

from app_students.forms import StudentSignupForm
from app_students.file_utils import uploaded_file
from app_students.mail_utils import send_welcome_mail

from students.models import User
from courses.models import Course, CourseProgress


class StudentRegistrationView(CreateView):
    model = User
    template_name = 'registration/signup_form.html'
    form_class = StudentSignupForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        print(self.request.GET.get('next'))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):

        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['email'], password=cd['password1'])
        login(self.request, user)
        
        send_welcome_mail(cd)

        return result

    def get_success_url(self):

        if self.request.GET.get('next'):
            return self.request.GET.get('next') + "#register=success"
        
        return reverse_lazy('cart_detail') + '?register=success'


class StudentHomeView(generic.TemplateView):
    template_name = 'student_home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentHomeView, self).get_context_data(
            *args, **kwargs)
        return context


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/list.html'

    def get_queryset(self):
        qs = super(CourseListView, self).get_queryset()

        qs = qs.filter(students__in=[self.request.user])

        print(self.request.GET.get('q', None))

        return qs


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/detail.html'

    def get_context_data(self, **kwargs):

        context = super(CourseDetailView,
                        self).get_context_data(**kwargs)

        student = self.request.user

        course = self.get_object()

        if not course.course_enrolled.filter(user=student).exists():
            context['not_found'] = True
            return context

        context['prev_completed'] = True
        context['module'] = None
        context['completed_contents'] = []
        context['taken_quizzes'] = []
        context['active_content'] = None
        context['next_content'] = None
        context['content_completed'] = True

        course_details = []
        modules_list = course.modules.all().order_by('order')

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

        if 'not_found' in context:
            return redirect('course_list')

        if context['module'] and (context['prev_completed'] == False or context['active_content'] == None):
            return redirect('student_course_detail', self.get_object().id)

        return super(CourseDetailView, self).render_to_response(context, **response_kwargs)

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


def file_upload(request):

    result = 0

    if request.method == 'POST' and request.FILES['file']:
        result = uploaded_file(request.FILES['file'])

    return HttpResponse(result)
