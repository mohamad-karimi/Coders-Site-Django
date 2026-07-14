from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        INSTRUCTOR = "instructor", "Instructor"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to="student/", default="student/default.jpg")

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
    )