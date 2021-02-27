from django.contrib import admin
from students.models import User
from students.models import Quiz
from students.models import Question
from students.models import Answer
# from students.models import Student
from students.models import TakenQuiz
from students.models import StudentAnswer
from students.models import Tag
from django.contrib.auth.admin import UserAdmin as uAdmin

class TagAdmin(admin.ModelAdmin):
    model = Tag

class AnswerInline(admin.StackedInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class UserAdmin(uAdmin):
    model = User
    fieldsets = (
        *uAdmin.fieldsets, 
        (                     
            'Other Options',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'is_student', 'is_teacher'
                ),
            },
        ),
    )
    list_display = ['username', 'first_name', 'last_name']
    list_filter = ['is_teacher', 'is_student', 'is_staff']

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Student)
admin.site.register(TakenQuiz)
admin.site.register(StudentAnswer)
admin.site.register(Tag, TagAdmin)
