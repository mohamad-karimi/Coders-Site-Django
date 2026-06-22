from django.db import models
from django.core.validators import FileExtensionValidator
from taggit.managers import TaggableManager
from instructor.models import Instructor

BEGINNER = "مقدماتی"
INTERMEDIATE = "متوسط"
ADVANCED = "حرفه ای"

LEVEL_CHOICES = (
    (BEGINNER, "مقدماتی"),
    (INTERMEDIATE, "متوسط"),
    (ADVANCED, "حرفه ای"),
)

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=50)
    price = models.PositiveIntegerField(default=0)
    discount_percent = models.PositiveSmallIntegerField(default=0)
    is_free = models.BooleanField(default=False)
    image = models.ImageField(upload_to='course/', default='course/default.jpg')
    short_description = models.CharField(max_length=120, null=True)
    overview = models.TextField()
    status = models.BooleanField(default=False)
    total_duration = models.PositiveIntegerField()
    skill_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, null=True)
    degree = models.CharField(max_length=50)
    tag = TaggableManager()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    published_date = models.DateTimeField(null=True,)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="courses", null=True)

    class Meta:
        ordering = ["-created_date"]
    
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

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(
        upload_to='lesson/',
        validators=[FileExtensionValidator(['mp4'])],
        null=True
    )
    duration = models.PositiveIntegerField()
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='lessons',
        null=True
    )

    def __str__(self):
        return self.title