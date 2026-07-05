from django.urls import path
from website.views import index, contact, about, faq, search, like_question

app_name = "website"

urlpatterns = [
    path('', index, name="home"),
    path('contact/', contact, name="contact"),
    path('about/', about, name="about"),
    path('faq/', faq, name="faq"),
    path('search/', search, name='search'),
    path("question/<int:id>/like/", like_question, name="like_question"),
]