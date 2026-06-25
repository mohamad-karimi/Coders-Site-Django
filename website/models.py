from django.db import models
import jdatetime
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
CATEGORY_CHOICES = [
    ("business", "کسب‌وکار"),
    ("development", "توسعه"),
    ("design", "طراحی"),
    ("marketing", "بازاریابی"),
    ("courses", "دوره‌ها"),
    ("start", "شروع"),
    ("profile", "حساب کاربری و پروفایل"),
]

class Contact(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.name
    
class Question(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="question")
    text = models.CharField(max_length=550)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]
    
    @property
    def jalali_date(self):
        return jdatetime.datetime.fromgregorian(
            datetime=timezone.localtime(self.created_date)
        ).strftime("%Y/%m/%d %H:%M")
    
    def __str__(self):
        return str(self.name)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer")
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")


    class Meta:
        ordering = ["-created_date"]
    
    @property
    def jalali_date(self):
        return jdatetime.datetime.fromgregorian(
            datetime=timezone.localtime(self.created_date)
        ).strftime("%Y/%m/%d %H:%M")
    
    def __str__(self):
        return str(self.question)
    
class MentorUser(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
    confirm_password = models.CharField(max_length=25)
    avatar = models.ImageField(upload_to='mentor/', default='mentor/default.jpg')
    expertise = models.CharField(max_length=50)

    def __str__(self):
        return self.name