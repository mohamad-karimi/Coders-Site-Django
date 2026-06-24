from django.urls import path
from website.views import index, contact, about, faq, error_404, search

app_name = "website"
urlpatterns = [
    path('', index, name="home"),
    path('contact/', contact, name="contact"),
    path('about/', about, name="about"),
    path('faq/', faq, name="faq"),
    path('404/', error_404, name="40"),
    path('search/', search, name='search'),
]