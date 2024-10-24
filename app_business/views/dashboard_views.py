from django.views import generic

class HomeView(generic.TemplateView):
    template_name = 'business_home/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(
            *args, **kwargs)

        return context