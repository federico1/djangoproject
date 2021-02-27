from django.shortcuts import render
from django.views import generic

class HomeView(generic.TemplateView):
    template_name = 'admin_home.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        return context


# class UsersView(generic.TemplateView):
#     template_name = 'admin_users.html'
    
#     def get_context_data(self, *args, **kwargs):
#         context = super(UsersView, self).get_context_data(*args, **kwargs)
#         return context