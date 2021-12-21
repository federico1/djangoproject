from django.urls import path
from .views import main_views

urlpatterns = [
    path('register/', main_views.StudentRegistrationView.as_view(),
         name='student_registration'),
    path('uploadfile', main_views.file_upload, name='upload-file'),
]
