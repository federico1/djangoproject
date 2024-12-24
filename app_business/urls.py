from django.urls import path
from django.views.decorators.cache import cache_page, never_cache
from .views import dashboard_views, employee_views, public_views, course_views, order_views, free_course_views

employee_views_urlpatterns = [path('employees/',
                                   never_cache(cache_page(60*60)
                                               (employee_views.EmployeesTemplateView.as_view())),
                                   name='business_employees'),
                              path('employees-manage/',
                                   never_cache(cache_page(60*60)
                                               (employee_views.EmployeesManageView.as_view())),
                                   name='business_employees_manage'),
                              path('employees/manage/<id>/',
                                   never_cache(cache_page(60*60)
                                               (employee_views.SingleEmployeeManageView.as_view())),
                                   name='business_employee_detail'),]

course_views_urlpatterns = [path('buy-courses/',
                                 never_cache(cache_page(60*60)
                                             (course_views.BuyCoursesTemplateView.as_view())),
                                 name='business_buy_courses'),
                            path('my-cart/',
                                 never_cache(cache_page(60*60)
                                             (course_views.MyCartTemplateView.as_view())),
                                 name='business_my_cart'),
                            path('my-checkout/',
                                 never_cache(cache_page(60*60)
                                             (course_views.CheckoutTemplateView.as_view())),
                                 name='business_my_checkout'),
                            path('my-checkout-post-order/',
                                 never_cache(cache_page(60*60)
                                             (course_views.CheckoutPostOrderView.as_view())),
                                 name='business_my_checkout_post_order'),
                            path('purchased-courses/',
                                 never_cache(cache_page(60*60)
                                             (course_views.MyCoursesTemplateView.as_view())),
                                 name='business_my_courses'),
                            path('purchased-courses-manage/',
                                 never_cache(cache_page(60*60)
                                             (course_views.MyCoursesManageView.as_view())),
                                 name='business_my_courses_manage'),]

order_views_urlpatterns = [path('order-history/', never_cache(cache_page(60*60)
                                                              (order_views.PurchaseHistoryView.as_view())),
                                name='business_purchase_history'),
                           path('purchase-invoice/<slug:ref>/<slug:item>/',
                                order_views.InvoiceView.as_view(), name='business_purchase_invoice'),
                           path('purchase-receipt/<slug:ref>/<slug:item>/',
                                order_views.ReceiptView.as_view(), name='business_purchase_receipt'),]

free_course_views_urlpatterns = [path('buy-free-courses/',
                                 never_cache(cache_page(60*60)
                                             (free_course_views.BuyFreeCoursesTemplateView.as_view())),
                                 name='business_buy_free_courses')]

urlpatterns = [
    path('dashboard/',
         dashboard_views.HomeView.as_view(),
         name='business_dashboard'),
    path('account-register/', never_cache(cache_page(60*60)
                                          (public_views.RegisterBusinessUserView.as_view())),
         name='business_user_register'),
] + employee_views_urlpatterns + course_views_urlpatterns + order_views_urlpatterns + free_course_views_urlpatterns
