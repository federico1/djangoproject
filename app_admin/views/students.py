from django.shortcuts import render
from django.views import generic


class StudentsView(generic.TemplateView):
    template_name = 'students/list.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(StudentsView, self).get_context_data(*args, **kwargs)
        return context


class EvaluationListView(generic.TemplateView):
    template_name = 'students/evaluation_list.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(EvaluationListView, self).get_context_data(*args, **kwargs)
        return context


class AssessmentView(generic.TemplateView):
    template_name = 'students/assessment.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(AssessmentView, self).get_context_data(*args, **kwargs)
        return context