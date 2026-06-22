from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

# Create your models here.
class Instructor(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True)
    image = models.ImageField(upload_to='instructor/', default='instructor/default.jpg')
    expertise = models.CharField(max_length=50)
    description = models.TextField()
    short_description = models.CharField(max_length=120, null=True)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    experience_of_the_year = models.PositiveIntegerField()
    # score

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            english_name = unidecode(self.name)
            base_slug = slugify(english_name)

            slug = base_slug
            counter = 1

            while Instructor.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

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