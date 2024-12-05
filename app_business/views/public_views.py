
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from compression_middleware.decorators import compress_page
from django.contrib.auth import authenticate, login

from students.models import User
from app_business.forms import BusinessUserSignupForm
from app_business.notifications import mail_welcome_bussiness_user


@method_decorator(compress_page, name="dispatch")
class RegisterBusinessUserView(CreateView):
    model = User
    template_name = 'business_public/register_business_user.html'
    form_class = BusinessUserSignupForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('course_list'))
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):

        result = super(RegisterBusinessUserView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['email'], password=cd['password1'])
        login(self.request, user)

        mail_welcome_bussiness_user(cd)

        return result
    
    def get_success_url(self):

        if self.request.GET.get('next'):
            return self.request.GET.get('next') + "#register=success"

        return reverse_lazy('cart_detail') + '?register=success'
