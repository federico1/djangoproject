from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from app_business.decorators import business_role_required

decorators = [login_required, business_role_required]
@method_decorator(decorators, name='dispatch')
class HomeView(generic.TemplateView):
    template_name = 'business_home/index.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(
            *args, **kwargs)

        return context