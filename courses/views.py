from django.views import generic
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic.base import TemplateResponseMixin, View
from django.db.models import Count
from .models import Subject, Course
from students.forms import CourseEnrollForm
from django.core.cache import cache


# class HomePage(generic.TemplateView):
#     template_name = "home.html"

obsele_subjects = {
  "csp-exam-prep-course": "csp",
}

class IndexView(TemplateResponseMixin, View):
    template_name = 'index.html'

    def get(self, request):
        courses = Course.objects.filter(is_deleted=False, mark_type='popular')
        return self.render_to_response({
            'courses': courses
        })


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
                subject = Subject.objects.get(slug=subject) #get_object_or_404(Subject, slug=subject)
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
                courses = all_courses.filter(owner=int(request.GET.get('teacher')))

        # instructors = User.objects.annotate(
        #                    total_courses=Count('courses_created')).filter(total_courses__gt=0)

            return self.render_to_response({'subjects': subjects,
                                            'subject': subject,
                                            'courses': courses,
                                            'instructors': None})
        except Subject.DoesNotExist:
            url = '/'
            if subject in obsele_subjects:
                url = (reverse('course_list_subject', kwargs={"subject": obsele_subjects[subject]}))
                print(url)
            return redirect(url)


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView,
                        self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})
        return context


class PostClassSurveryDetailView(generic.TemplateView):
    template_name = 'courses/post_survery.html'

    def get_context_data(self, **kwargs):
        context = super(PostClassSurveryDetailView,
                        self).get_context_data(**kwargs)

        # context['enroll_form'] = CourseEnrollForm(
        #                            initial={'course':self.object})
        return context
