from django.db import models
from taggit.managers import TaggableManager
from django.utils import timezone
import jdatetime
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()

# Create your models here.
COLOR_CHOICES = [
    ('primary', 'آبی'),
    ('success', 'سبز'),
    ('danger', 'قرمز'),
    ('warning', 'زرد'),
    ('info', 'فیروزه‌ای'),
    ('secondary', 'خاکستری'),
    ('orange', 'نارنجی'),
    ('purple', 'بنفش'),
]

class Category(models.Model):
    name = models.CharField(max_length=150)
    color = models.CharField(choices=COLOR_CHOICES, default='primary')

    def __str__(self):
        return self.name
    
def post_media_upload_path(instance, filename):
    return f"blog/post_{instance.slug}/{filename}"
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True, max_length=255)
    info = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    content = RichTextUploadingField()
    content2 = RichTextUploadingField(null=True)
    image = models.ImageField(upload_to=post_media_upload_path, default="blog/image/default.jpg")
    video = models.FileField(upload_to=post_media_upload_path, validators=[FileExtensionValidator(['mp4'])])
    tag = TaggableManager()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="post")
    views = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    status = models.BooleanField(default= False)
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @property
    def jalali_date(self):
        return jdatetime.datetime.fromgregorian(
            datetime=self.created_date
        ).strftime("%Y/%m/%d")
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

            base = self.slug
            counter = 1

            while Post.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_date"]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:blog_detail", args=[self.slug])

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_comments") 
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment") 
    published =models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
    
    @property
    def jalali_date(self):
        return jdatetime.datetime.fromgregorian(
            datetime=timezone.localtime(self.created_date)
        ).strftime("%Y/%m/%d %H:%M")
    
    def __str__(self):
        return str(self.author)
    
class ReplayComment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_replies")
    comment = models.TextField()
    question_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="blog_replies") 
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
    
    @property
    def jalali_date(self):
        return jdatetime.datetime.fromgregorian(
            datetime=timezone.localtime(self.created_date)
        ).strftime("%Y/%m/%d %H:%M")
    
    def __str__(self):
        return str(self.author)