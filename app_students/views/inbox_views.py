from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app_students.decorators import ISStudentUserMixin


@method_decorator([login_required], name='dispatch')
class MessagesView(ISStudentUserMixin, TemplateView):
    template_name = "inbox/messages.html"

    def get_context_data(self, **kwargs):
        context = super(MessagesView, self).get_context_data(**kwargs)
        return context