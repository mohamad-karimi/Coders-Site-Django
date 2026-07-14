from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Instructor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="instructor", null=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='instructor/', default='instructor/default.jpg')
    counted_views = models.IntegerField(default=0)
    expertise = models.CharField(max_length=200)
    description = RichTextUploadingField()
    short_description = models.CharField(max_length=120)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    experience_of_the_year = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            full_name = f"{self.user.first_name}-{self.user.last_name}"
            self.slug = slugify(full_name, allow_unicode=True)
            base = self.slug
            counter = 1

            while Instructor.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["user__username"]

    @property
    def instructor_avg_score(self):
        avg = self.courses.aggregate(
            avg=models.Avg("score__score")
        )["avg"] or 0

        return round(avg * 2) / 2

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("instructor:instructor_single", args=[self.slug])
    
class Education(models.Model):
    university = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=200)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="educations")

    def __str__(self):
        return self.university

class Skill(models.Model):
    name = models.CharField(max_length=200)
    amount = models.PositiveSmallIntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="skills")

    def __str__(self):
        return self.name