from django.views import generic
from app_students.decorators import ISStudentUserMixin


class EditProfileView(ISStudentUserMixin, generic.TemplateView):
    template_name = 'profile/edit.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(EditProfileView, self).get_context_data(
            *args, **kwargs)
        return context


class SwitchBusinessAccountView(ISStudentUserMixin, generic.TemplateView):
    template_name = 'profile/switch_business.html'

    
    def get_context_data(self, *args, **kwargs):
        context = super(SwitchBusinessAccountView, self).get_context_data(
            *args, **kwargs)
        return context