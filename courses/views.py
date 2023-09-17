from django.views import generic
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic.base import TemplateResponseMixin, View
from django.db.models import Count
from .models import Subject, Course
from students.forms import CourseEnrollForm
from django.core.cache import cache
from django.utils.decorators import method_decorator
from compression_middleware.decorators import compress_page
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.vary import vary_on_cookie

from datetime import datetime

# class HomePage(generic.TemplateView):
#     template_name = "home.html"

obsele_subjects = {
    "csp": "csp-exam-prep",
}


@method_decorator(compress_page, name="dispatch")
@method_decorator(cache_page(1), name='dispatch')
@method_decorator(vary_on_cookie, name='dispatch')
#@method_decorator([never_cache,], name="dispatch")
class IndexView(TemplateResponseMixin, View):
    template_name = 'index.html'

    def get(self, request):
        
        courses = cache.get('home_popular')
        
        if not courses:
            courses = Course.objects.filter(is_deleted=False, mark_type='popular')[:4]
            cache.set('home_popular', courses)

        
        return self.render_to_response({
            'courses': courses
        })


@method_decorator(compress_page, name="dispatch")
@method_decorator(cache_page(1), name='dispatch')
@method_decorator([never_cache,], name="dispatch")
class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request, subject=None):
        try:
            subjects = cache.get('all_subjects')

            if not subjects:
                subjects = Subject.objects.annotate(
                    total_courses=Count('courses'))
                cache.set('all_subjects', subjects)

            all_courses = Course.objects.annotate(
                total_modules=Count('modules'))

            if subject:
                # get_object_or_404(Subject, slug=subject)
                subject = subjects.get(slug=subject)
                key = 'subject_{}_courses'.format(subject.id)
                courses = cache.get(key)

                if not courses:
                    courses = all_courses.filter(subject=subject)
                    cache.set(key, courses)
            else:
                courses = cache.get('all_courses')
                if not courses:
                    courses = all_courses
                    cache.set('all_courses', courses)

            if request.GET.get('q') is not None:
                courses = all_courses.filter(
                    title__icontains=str(request.GET.get('q')))

            if request.GET.get('teacher') is not None:
                courses = all_courses.filter(
                    owner=int(request.GET.get('teacher')))

        # instructors = User.objects.annotate(
        #                    total_courses=Count('courses_created')).filter(total_courses__gt=0)

            return self.render_to_response({'subjects': subjects,
                                            'subject': subject,
                                            'courses': courses,
                                            'instructors': None,
                                            'page_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            })
        except Subject.DoesNotExist:
            url = '/'
            print(subject)
            if subject in obsele_subjects:
                url = (reverse('course_list_subject', kwargs={
                       "subject": obsele_subjects[subject]}))
                print(url)
            return redirect(url)


@method_decorator(compress_page, name="dispatch")
class CourseListViewV2(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list_v2.html'

    def get(self, request, subject=None):
        try:
            
            subjects = Subject.objects.annotate(
                    total_courses=Count('courses'))

            all_courses = Course.objects.annotate(
                total_modules=Count('modules'))

            if subject:
                subject = Subject.objects.get(slug=subject)
                courses = all_courses.filter(subject=subject)
            else:
                courses = all_courses

            if request.GET.get('q') is not None:
                courses = all_courses.filter(
                    title__icontains=str(request.GET.get('q')))

            if request.GET.get('teacher') is not None:
                courses = all_courses.filter(
                    owner=int(request.GET.get('teacher')))

        # instructors = User.objects.annotate(
        #                    total_courses=Count('courses_created')).filter(total_courses__gt=0)

            return self.render_to_response({'subjects': subjects,
                                            'subject': subject,
                                            'courses': courses,
                                            'instructors': None,
                                            'page_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            })
        except Subject.DoesNotExist:
            url = '/'
            print(subject)
            if subject in obsele_subjects:
                url = (reverse('course_list_subject', kwargs={
                       "subject": obsele_subjects[subject]}))
                print(url)
            return redirect(url)


@method_decorator(compress_page, name="dispatch")
class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView,
                        self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})
        return context


@method_decorator(compress_page, name="dispatch")
@method_decorator(never_cache, name="dispatch")
class PostClassSurveryDetailView(generic.TemplateView):
    template_name = 'courses/post_survery.html'

    def get_context_data(self, **kwargs):
        context = super(PostClassSurveryDetailView,
                        self).get_context_data(**kwargs)

        # context['enroll_form'] = CourseEnrollForm(
        #                            initial={'course':self.object})
        return context
