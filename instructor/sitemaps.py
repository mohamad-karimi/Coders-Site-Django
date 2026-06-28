from django.contrib.sitemaps import Sitemap
from .models import Instructor

class InstructorSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7
    protocol = "https"

    def items(self):
        return Instructor.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()