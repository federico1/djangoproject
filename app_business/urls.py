from django.urls import path
from django.views.decorators.cache import cache_page, never_cache
from .views import dashboard_views, employee_views, public_views, course_views


urlpatterns = [
    path('dashboard/',
         dashboard_views.HomeView.as_view(),
         name='business_dashboard'),
    path('employees/',
         never_cache(cache_page(10)
                     (employee_views.EmployeesTemplateView.as_view())),
         name='business_employees'),
    path('employees-manage/',
         never_cache(cache_page(10)
                     (employee_views.EmployeesManageView.as_view())),
         name='business_employees_manage'),
    path('employees/manage/<id>/',
         employee_views.SingleEmployeeManageView.as_view(),
         name='business_employee_detail'),
    path('buy-courses/',
         course_views.BuyCoursesTemplateView.as_view(),
         name='business_buy_courses'),
    path('my-cart/',
         course_views.MyCartTemplateView.as_view(),
         name='business_my_cart'),
    path('my-checkout/',
         course_views.CheckoutTemplateView.as_view(),
         name='business_my_checkout'),
    path('my-checkout-post-order/',
         course_views.CheckoutPostOrderView.as_view(),
         name='business_my_checkout_post_order'),
    path('purchased-courses/',
         course_views.MyCoursesTemplateView.as_view(),
         name='business_my_courses'),
    path('purchased-courses-manage/',
         course_views.MyCoursesManageView.as_view(),
         name='business_my_courses_manage'),
    path('account-register/', public_views.RegisterBusinessUserView.as_view(),
         name='business_user_register'),
]
