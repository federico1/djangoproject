from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from braces.views import LoginRequiredMixin
from django.views.generic.detail import DetailView

from .models import Conversation

@method_decorator([login_required], name='dispatch')
class MessagesView(TemplateView):
    template_name = "messages.html"
    
    def get_context_data(self, **kwargs):
       context = super(MessagesView, self).get_context_data(**kwargs)
       context['conversation'] = None

       if 'pk' in self.kwargs:
           context['conversation'] = Conversation.objects.get(pk=self.kwargs['pk'])
       return context