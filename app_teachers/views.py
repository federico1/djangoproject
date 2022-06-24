from operator import le
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, \
    DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.forms.models import modelform_factory
from django.apps import apps
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.db.models import Count
from django.core.cache import cache
from django.http import HttpResponse
from django.utils.text import slugify
from django.core import serializers

from courses.models import Subject, Course, Module, Content, CourseProgress
from .forms import ModuleFormSet
from students.forms import CourseEnrollForm
from students.models import User, Quiz


class OwnerMixin(object):
    def get_queryset(self):
        
        qs = super(OwnerMixin, self).get_queryset()

        if 'q' in self.request.GET:
            qs = qs.filter(title__icontains=self.request.GET['q'])
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview','is_free', 'price', 'discounted_price', 'owner_id']
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'manage/course/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_json'] = serializers.serialize('json', self.object_list)
        return context


class CourseCreateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
    template_name = 'manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'manage/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'manage/content/form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file', 'iframe']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)

        return super(ContentCreateUpdateView,
                     self).dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:

                Content.objects.create(module_id=self.module.id,
                                       item=obj)
            return redirect('module_content_list', self.module.id)

        return self.render_to_response({'form': form,
                                        'object': self.obj})


class ContentDeleteView(View):

    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)

        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin,
                      JsonRequestResponseMixin,
                      View):
    def post(self, request):
        print(self.request_json)
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                                  course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin,
                       JsonRequestResponseMixin,
                       View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                                   module__course__owner=request.user) \
                .update(order=order)
        return self.render_json_response({'saved': 'OK'})


class TeacherHomeView(generic.TemplateView):
    template_name = 'teacher_home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(TeacherHomeView, self).get_context_data(
            *args, **kwargs)

        context['courses_count'] = self.request.user.courses_created.count()

        users_id = list(self.request.user.courses_created.values_list('students',
                                                                      flat=True))
        users_id = list(filter(lambda id: id is not None and id > 0, users_id))
        
        #students_count = users_id #User.objects.filter(id__in=users_id).count()

        context['students_count'] = len(users_id)

        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course_detail/index.html'
    
    def get_queryset(self):
        qs = super(CourseDetailView, self).get_queryset()
        return qs

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView,self).get_context_data(**kwargs)

        course = self.get_object()

        context['module'] = None
        context['quiz'] = None

        if 'module_id' in self.kwargs and self.request.GET.get('content'):

            context['module'] = course.modules.get(id=self.kwargs['module_id'])

            if self.request.GET.get('type') == 'quiz':
                 context['quiz'] = Quiz.objects.get(pk=self.request.GET.get('content'))

        return context


class QuizTemplateView(TemplateResponseMixin, View):
    template_name = 'manage/quiz/list.html'

    def get(self, request):
        return self.render_to_response({})


class MessagesView(generic.TemplateView):
    template_name = "messages.html"

    def get_context_data(self, **kwargs):
        context = super(MessagesView, self).get_context_data(**kwargs)
        return context


class Students(generic.TemplateView):
    template_name = 'students/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super(Students,
                        self).get_context_data(*args, **kwargs)
        return context


def CourseCopy(request):
    result = 0
    if request.method == 'POST' and request.POST['id']:
        course_object = Course.objects.get(pk=request.POST['id'])

        modules = course_object.modules.all()

        course_object.pk = None
        course_object.id = None

        if request.POST['name']:
            course_object.title = request.POST['name']

        old_slug = course_object.slug
        course_object.slug = slugify(course_object.title)

        if old_slug and old_slug == course_object.slug:
            course_object.slug = course_object.slug + '-copied'

        course_object.save()

        for mod in modules:

            contents = mod.contents.all()
            mod.pk = None
            mod.id = None
            mod.course = course_object
            mod.save()

            for content in contents:

                content_item = None

                if content.item:
                    content_item = content.item
                    content_item.pk = None
                    content_item.id = None
                    content_item.save()

                Content.objects.create(module_id=mod.id, item=content_item)

        result = course_object.id

    return HttpResponse(result, content_type='text/plain')


def ModuleCopy(request):
    result = 0
    if request.method == 'POST' and request.POST['id'] and request.POST['course']:
        module_object = Module.objects.get(pk=request.POST['id'])
        contents = module_object.contents.all()

        module_object.pk = None
        module_object.id = None

        if request.POST['name']:
            module_object.title = request.POST['name']

        module_object.course_id = request.POST['course']
        module_object.save()

        for content in contents:
            content_item = None

            if content.item:

                content_item = content.item
                content_item.pk = None
                content_item.id = None
                content_item.save()

                Content.objects.create(module_id=module_object.id, item=content_item)
        
        result = module_object.id

    return HttpResponse(result, content_type='text/plain')
