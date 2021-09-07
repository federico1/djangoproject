from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from courses.models import Course, Subject

class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        items_list = ['about_detail', 'legal_detail', 'contact_detail', 'student_manual_detail', 'faq', 'sst_verify']
        items_list = items_list + ['login', 'courses_list']
        return items_list
    
    def location(self, item):
        return reverse(item)

class SubjectsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        subject_list = Subject.objects.all()
        return subject_list


class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        item = Course.objects.all()
        return item