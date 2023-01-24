from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from courses.models import Course, Subject

class StaticViewSitemap(Sitemap):
    changefreq = "hourly"

    def items(self):
        items_list = ['course_list', 'about_detail', 'privacy_policy', 'terms', 'refund', 'contact_detail', 'faq', 'sst_verify']
        items_list = items_list + ['login', 'courses_list']
        return items_list
    
    def location(self, item):
        return reverse(item)


class SubjectsSitemap(Sitemap):
    changefreq = "hourly"

    def items(self):
        subject_list = Subject.objects.all()
        return subject_list

    def location(self, obj):
        url = obj.get_absolute_url()
        return url if len(url)>0 and url[-1]=='/' else url + '/'

class CourseSitemap(Sitemap):
    changefreq = "hourly"

    def items(self):
        item = Course.objects.all()
        return item

    def location(self, obj):
        url = obj.get_absolute_url()
        return url if len(url)>0 and url[-1]=='/' else url + '/'