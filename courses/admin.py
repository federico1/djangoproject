from django.contrib import admin
from .models import Subject, Course, Module
from app_cart.models import *


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]


@admin.register(BusinessUserCredit)
class BusinessUserCreditAdmin(admin.ModelAdmin):
    list_display = ('user', 'credits_purchased',
                    'credits_remaining', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at',)
