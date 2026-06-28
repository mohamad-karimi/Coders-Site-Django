from django.contrib.sitemaps import Sitemap
from .models import Course

class CourseSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9
    protocol = "https"

    def items(self):
        return Course.objects.filter(status=True)

    def lastmod(self, obj):
        return obj.published_date
    
    def location(self, obj):
        return obj.get_absolute_url()