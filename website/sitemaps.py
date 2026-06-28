from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "daily"
    protocol = 'https'

    def items(self):
        return ["website:home", "website:about", "website:contact", "website:faq"]

    def location(self, item):
        return reverse(item)