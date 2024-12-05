"""educa URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from courses.views import CourseListView, IndexView
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import url
from django.contrib.sitemaps.views import sitemap
from django.conf.urls import (handler400, handler403, handler404, handler500)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.decorators.cache import cache_page, never_cache
from django.views.generic.base import TemplateView

from .sitemap import StaticViewSitemap, SubjectsSitemap, CourseSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'subjects': SubjectsSitemap,
    'course': CourseSitemap
}

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAdminUser],
)

urlpatterns = [
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('admin/', admin.site.urls),
    path('course/', include('courses.urls')),
    path('courses', CourseListView.as_view(), name='courses_list'),
    path('', (IndexView.as_view()), name='course_list'),
    path('teachers/', include('app_teachers.urls')),
    path('quiz/', include('app_quiz.urls')),
    path('communicate/', include('app_chat.urls')),
    path('dashboard/', include('app_admin.urls')),
    url(r'api/', include('app_api.urls')),
    url(r'api/', include('app_api_v2.urls')),
    url(r'api/backend/', include('app_api_backend_v1.urls')),
    path('', include('app_public.urls')),
    path('', include('app_cart.urls')),
    path('students/', include('app_students.urls')),
    path('business/', include('app_business.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path("robots.txt",TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

if not settings.DEBUG:
    handler400 = 'app_public.views.bad_request'
    handler403 = 'app_public.views.bad_request'
    handler404 = 'app_public.views.bad_request'
    handler500 = 'app_public.views.bad_request'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
