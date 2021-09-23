from django.views import generic

class CartView(generic.TemplateView):
    template_name = "cart.html"