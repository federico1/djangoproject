from django.urls import path
from .views import PrivacyPolicyView, AboutView, ContactView, StudentManualView, FaqView, PackagesView, RefundView, TermsView
from .more_views.views_sst import SSTVerifyView

urlpatterns = [
    path('privacy-policy/',
         PrivacyPolicyView.as_view(),
         name='privacy_policy'),
    path('terms-conditions/',
         TermsView.as_view(),
         name='terms'),
    path('refund-policy/',
         RefundView.as_view(),
         name='refund'),
    path('about/',
         AboutView.as_view(),
         name='about_detail'),
    path('contact/',
         ContactView.as_view(),
         name='contact_detail'),
#     path('student-manual/',
#          StudentManualView.as_view(),
#          name='student_manual_detail'),
    path('sst-verify/',
         SSTVerifyView.as_view(),
         name='sst_verify'),
    path('faq/',
         FaqView.as_view(),
         name='faq'),
    path('packages/',
         PackagesView.as_view(),
         name='packages'),
]
