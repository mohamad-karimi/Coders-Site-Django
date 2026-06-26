from django.db import models
from django.core.validators import FileExtensionValidator
from taggit.managers import TaggableManager
from instructor.models import Instructor
from django.utils.text import slugify
from django.utils import timezone
import jdatetime
from django.contrib.auth import get_user_model

User = get_user_model()

BEGINNER = "مقدماتی"
INTERMEDIATE = "متوسط"
ADVANCED = "حرفه‌ای"

LEVEL_CHOICES = (
    (BEGINNER, "مقدماتی"),
    (INTERMEDIATE, "متوسط"),
    (ADVANCED, "حرفه‌ای"),
)

SCORE_CHOICES = [
    (1, "★☆☆☆☆"),
    (2, "★★☆☆☆"),
    (3, "★★★☆☆"),
    (4, "★★★★☆"),
    (5, "★★★★★"),
]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to='course/', default='course/category/default.svg')
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    discount_percent = models.PositiveSmallIntegerField(default=0)
    discount_end = models.DateTimeField(null=True, blank=True)
    is_free = models.BooleanField(default=False)
    image = models.ImageField(upload_to='course/', default='course/default.jpg')
    short_description = models.CharField(max_length=120)
    overview = models.TextField()
    status = models.BooleanField(default=False)
    total_duration = models.PositiveIntegerField()
    counted_views = models.IntegerField(default=0)
    skill_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    degree = models.CharField(max_length=50)
    tag = TaggableManager()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="courses")

    class Meta:
        ordering = ["-created_date"]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)

            base = self.slug
            counter = 1

            while Instructor.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    @property
    def final_price(self):
        return self.price - (self.price * self.discount_percent // 100)

    def __str__(self):
        return self.title
    
    @property
    def lessons_count(self):
        return Lesson.objects.filter(
            section__course=self
        ).count()

class Section(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='sections'
    )

    def __str__(self):
        return self.title

def lesson_upload_path(instance, filename):
    return f"lesson/course_{instance.section.course.slug}/{filename}"

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(
        upload_to=lesson_upload_path,
        validators=[FileExtensionValidator(['mp4'])],
    )
    duration = models.PositiveIntegerField()
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='lessons',
    )

    def __str__(self):
        return self.title
    
class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="scores")
    score = models.PositiveSmallIntegerField(choices=SCORE_CHOICES)
    comment = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="score")
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        unique_together = ('user', 'course')
    
    @property
    def jalali_date(self):
        return jdatetime.datetime.fromgregorian(
            datetime=self.created_date
        ).strftime("%Y/%m/%d")
    
    def __str__(self):
        return f"{self.name} - {self.score}"
    
class Reply(models.Model):
    score = models.ForeignKey(Score, on_delete=models.CASCADE, related_name="replies")
    name = models.CharField(max_length=50)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    comment = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comment") 
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replaycomment")
    comment = models.TextField()
    question_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replaycomment") 
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
    
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="enrollment")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollment") 
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"
    
class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress")
    is_completed = models.BooleanField(default=False)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user} - {self.lesson}"
    
class CourseProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="course_progress")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="progress")

    is_completed = models.BooleanField(default=False)
    certificate_received = models.BooleanField(default=False)

    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} - {self.course}"