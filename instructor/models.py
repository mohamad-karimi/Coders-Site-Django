from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Instructor(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='instructor/', default='instructor/default.jpg')
    counted_views = models.IntegerField(default=0)
    expertise = models.CharField(max_length=50)
    description = RichTextUploadingField()
    short_description = models.CharField(max_length=120)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    experience_of_the_year = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)

            base = self.slug
            counter = 1

            while Instructor.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base}-{counter}"
                counter += 1

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]

    @property
    def instructor_avg_score(self):
        avg = self.courses.aggregate(
            avg=models.Avg("score__score")
        )["avg"] or 0

        return round(avg * 2) / 2

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("instructor:instructor_single", args=[self.slug])
    
class Education(models.Model):
    university = models.CharField(max_length=50)
    field_of_study = models.CharField(max_length=50)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="educations")

    def __str__(self):
        return self.university

class Skill(models.Model):
    name = models.CharField(max_length=50)
    amount = models.PositiveSmallIntegerField()
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name="skills")

    def __str__(self):
        return self.name