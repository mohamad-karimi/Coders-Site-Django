from django.db import models
from taggit.managers import TaggableManager
from django.utils import timezone
from django.contrib.auth.models import User
import jdatetime
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify

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
    name = models.CharField(max_length=50)
    color = models.CharField(choices=COLOR_CHOICES, default='primary')

    def __str__(self):
        return self.name
    
def post_media_upload_path(instance, filename):
    return f"blog/post_{instance.slug}/{filename}"
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    info = models.CharField(max_length=250, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    content = models.TextField()
    content2 = models.TextField(null=True)
    image = models.ImageField(upload_to=post_media_upload_path, default="blog/image/default.jpg")
    video = models.FileField(upload_to=post_media_upload_path, validators=[FileExtensionValidator(['mp4'])], null=True)
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
    
class Comment(models.Model):
    author = models.CharField(max_length=50)
    email = models.EmailField()
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comment") 
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