import datetime
import os
import random
import string

from django.views import generic
from django.views.generic.edit import CreateView
from braces.views import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from django import template

from django.utils.decorators import method_decorator
from xhtml2pdf import pisa
from xhtml2pdf.config.httpconfig import httpConfig

from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.vary import vary_on_cookie

from app_students.forms import StudentSignupForm, CompanySignupForm
from app_students.file_utils import uploaded_file, get_client_ip
from app_students.mail_utils import send_welcome_mail
from students.decorators import student_required

from students.models import User
from courses.models import Course, CourseProgress, StudentCertificate

register = template.Library()

@method_decorator(never_cache, name="dispatch")
class StudentRegistrationView(CreateView):
    model = User
    template_name = 'registration/signup_form.html'
    form_class = StudentSignupForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
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

@method_decorator(cache_page(2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class StudentHomeView(generic.TemplateView):
    template_name = 'student_home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StudentHomeView, self).get_context_data(
            *args, **kwargs)
        return context


@method_decorator(cache_page(2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/list.html'

    def get_queryset(self):
        qs = super(CourseListView, self).get_queryset()

        qs = qs.filter(students__in=[self.request.user])

        q = self.request.GET.get('q', None)
        id = self.request.GET.get('id', None)

        if q is not None:
            qs = qs.filter(title__icontains=q)

        if id is not None:
            qs = qs.filter(id=id)

        return qs


@method_decorator(cache_page(2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/detail.html'

    def get_context_data(self, **kwargs):

        context = super(CourseDetailView,
                        self).get_context_data(**kwargs)

        student = self.request.user

        course = self.get_object()

        enrollment = course.course_enrolled.filter(user=student)

        if not enrollment.exists():
            context['not_found'] = True
            return context

        context['prev_completed'] = True
        context['module'] = None
        context['completed_contents'] = []
        context['taken_quizzes'] = []
        context['active_content'] = None
        context['next_content'] = None
        context['content_completed'] = True
        context['enrollment'] = enrollment.first()
        context['user_ip'] = get_client_ip(self.request)
        context['course_tree'] = None

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
            module_id = int(self.kwargs['module_id'])
            context['module'] = course.modules.get(id=self.kwargs['module_id'])

            if self.request.GET.get('type') == 'quiz':
                context['active_content'] = [x for
                                             x in course_details if x['object'].id == content_id and x['module'].id == module_id and x['type'] == 'quiz'][0]
            else:
                context['active_content'] = [x for
                                             x in course_details if x['object'].id == content_id and x['type'] == 'content'][0]

            if self.request.GET.get('type') == 'quiz':
                current_index = [ix for ix, x in enumerate(
                    course_details) if x['object'].id == content_id and x['module'].id == module_id and x['type'] == 'quiz'][0]
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
                                         'object': course.quiz, 'score': score, 'module': context['module'], 'complete': True if course.quiz.id in taken_quizzes else False}

        context['course_tree'] = course_details

        return context


    def render_to_response(self, context, **response_kwargs):

        if 'not_found' in context:
            return redirect('course_list')

        if context['module'] and (context['prev_completed'] == False or context['active_content'] == None):
            return redirect('student_course_detail', self.get_object().id)

        return super(CourseDetailView, self).render_to_response(context, **response_kwargs)

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

@method_decorator(cache_page(2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class CourseCertificateDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'certificate/certificate.html'

    def get_context_data(self, **kwargs):

        context = super(CourseCertificateDetailView,
                        self).get_context_data(**kwargs)

        context['certificate_valid'] = True
        student = self.request.user
        course = self.get_object()
        enrolled = course.course_enrolled.filter(user=student)

        if not enrolled.exists() or enrolled.last().is_completed == False:
            context['certificate_valid'] = False

        return context

    def render_to_response(self, context, **response_kwargs):
        return super(CourseCertificateDetailView, self).render_to_response(context, **response_kwargs)

@method_decorator(cache_page(2), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
class CertificateTemplateDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'certificate/certificate_template.html'

    def get_context_data(self, **kwargs):

        context = super(CertificateTemplateDetailView,
                        self).get_context_data(**kwargs)

        context['certificate_valid'] = True
        student = self.request.user
        course = self.get_object()
        enrolled = course.course_enrolled.filter(user=student)

        if not enrolled.exists() or enrolled.last().is_completed == False:
            context['certificate_valid'] = False

        if context['certificate_valid'] == True:

            enrolled_last = enrolled.last()

            context['student_name'] = student.first_name + \
                ' ' + student.last_name
            completed_date = enrolled_last.completed_date
            context['completed_date'] = completed_date.strftime('%m/%d/%Y')

            if enrolled_last.certificates.count() <=0:
                certificate = StudentCertificate(
                course=course, user=student, enrollment=enrolled_last)
                certificate.add_new_certificate()

                context['ref_number'] = certificate.ref_number
            else:
                context['ref_number'] = enrolled_last.certificates.first().ref_number
        
        first_feature = course.features.first()
        credits = first_feature.credits if first_feature is not None else None
        
        context['credits'] = credits if credits is not None else ''
        context['sign_image'] = '/static/cert-files/image002.png'

        return context

    def render_to_response(self, context, **response_kwargs):

        if context['certificate_valid'] == False:
            return redirect('course_list')

        return super(CertificateTemplateDetailView, self).render_to_response(context, **response_kwargs)

@method_decorator(never_cache, name="dispatch")
class CompanyRegistrationView(CreateView):
    model = User
    template_name = 'registration/signup_company_form.html'
    form_class = CompanySignupForm

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):

        result = super(CompanyRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['email'], password=cd['password1'])
        login(self.request, user)

        #send_welcome_mail(cd)

        return result

    def get_success_url(self):

        if self.request.GET.get('next'):
            return self.request.GET.get('next') + "#register=success"

        return reverse_lazy('cart_detail') + '?register=success'


@login_required
@student_required
def download_certificate(request, pk):
    try:
        student = request.user
        course = Course.objects.get(pk=pk)
        enrolled = course.course_enrolled.filter(user=student)

        if enrolled.exists() or enrolled.last().is_completed == True:

            enrolled_last = enrolled.last()

            certificate = None

            if enrolled_last.certificates.count() <=0:
                return HttpResponse("We are unable to create your certificate. Please contact to support.")
            else:
                certificate = enrolled_last.certificates.first()

            student_name = student.first_name + \
                ' ' + student.last_name
            completed_date = enrolled_last.completed_date.strftime('%m/%d/%Y')

            template_path = 'certificate/certificate_template.html'

            sign_image = os.path.realpath(os.path.dirname(
                'static')) + '\courses\static\cert-files\image003.png'

            sign_image = 'https://pdhsafety.com/static/cert-files/image003.png'

            ref_number = certificate.ref_number

            context = {'certificate_valid': True,
                       'student_name': student_name, 'completed_date': completed_date, 'object': course,
                       'ref_number': ref_number, 'sign_image': sign_image}

            template = get_template(template_path)
            html = template.render(context)

            file_name = datetime.datetime.now().strftime("%y%m%d-%H%M%S") + "-" + \
                ref_number + "-certificate.pdf"
            file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', file_name)
            result_file = open(file_path, "w+b")

            httpConfig.save_keys('nosslcheck', True)
            pisa_status = pisa.CreatePDF(html, dest=result_file)
            result_file.close()

            ref_file_path = os.path.join(
                settings.MEDIA_URL, 'uploads', file_name)

            # certificate_object = StudentCertificate(
            #     course=course, user=student, ref_number=ref_number, file_path=ref_file_path)

            # certificate_object.save()

            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename="' + \
                    course.title+' Certificate.pdf"'
                return response
                # attachment

            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return HttpResponse(0)
    except Exception as ex:
        return HttpResponse(ex)


def file_upload(request):

    result = 0

    if request.method == 'POST' and request.FILES['file']:
        result = uploaded_file(request.FILES['file'])

    return HttpResponse(result)
