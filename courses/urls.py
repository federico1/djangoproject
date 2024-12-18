from django.urls import path
from . import views
from django.views.decorators.cache import cache_page, never_cache

urlpatterns = [
    path('subject/<slug:subject>/',
         never_cache(cache_page(60*60)(views.CourseListView.as_view())),
         name='course_list_subject'),
    path('post-survery/',
         views.PostClassSurveryDetailView.as_view(),
         name='course_post_survey'),
    path('<slug:slug>/',
         never_cache(cache_page(60*60)(views.CourseDetailView.as_view())),
         name='course_detail'),

]
