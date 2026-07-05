"""
URL configuration for coders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from website.sitemaps import StaticViewSitemap
from course.sitemaps import CourseSitemap
from blog.feeds import BlogFeed
from course.feeds import CourseFeed
from django.views.static import serve

handler404 = 'website.views.error_404'

sitemaps = {
    "static": StaticViewSitemap,
    "blog" : PostSitemap,
    "course": CourseSitemap,
}


urlpatterns = [
    path('admin-1389/', admin.site.urls),
    path('', include('website.urls')),
    path('instructor/', include('instructor.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('course/', include('course.urls')),
    path('blog/', include('blog.urls')),
    path('', include('authentication.urls')),
    path("sitemap.xml",sitemap,{"sitemaps": sitemaps},name="django.contrib.sitemaps.views.sitemap",),
    path("robots.txt", include("robots.urls")),
]

urlpatterns += [
    path("ckeditor/", include("ckeditor_uploader.urls")),
]

urlpatterns += [
    path("rss/blog/", BlogFeed()),
    path("rss/course/", CourseFeed()),
]

if settings.DEBUG:
    urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT
        )
    
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]