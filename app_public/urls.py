from django.urls import path
from django.views.decorators.cache import cache_page, never_cache
from .views import PrivacyPolicyView, AboutView, ContactView, FaqView, PackagesView, RefundView, TermsView, BusinessAccountFeaturesView, post_contact_form
from .more_views.views_sst import SSTVerifyView

urlpatterns = [
    path('privacy-policy/',
         never_cache(cache_page(60*60)(PrivacyPolicyView.as_view())),
         name='privacy_policy'),
    path('terms-conditions/',
         never_cache(cache_page(60*60)(TermsView.as_view())),
         name='terms'),
    path('refund-policy/',
         never_cache(cache_page(60*60)(RefundView.as_view())),
         name='refund'),
    path('about/',
         never_cache(cache_page(60*60)(AboutView.as_view())),
         name='about_detail'),
    path('contact/',
         never_cache(cache_page(60*60)(ContactView.as_view())),
         name='contact_detail'),
#     path('student-manual/',
#          StudentManualView.as_view(),
#          name='student_manual_detail'),
    path('sst-verify/',
         never_cache(cache_page(60*60)(SSTVerifyView.as_view())),
         name='sst_verify'),
    path('faq/',
         never_cache(cache_page(60*60)(FaqView.as_view())),
         name='faq'),
    path('packages/',
         never_cache(cache_page(60*60)(PackagesView.as_view())),
         name='packages'),
    path('business-account-features/',
         BusinessAccountFeaturesView.as_view(),
         name='business_account_features'),

    path(r'handle-ct-fm/',
         post_contact_form, name='post_contact_form'),
]
