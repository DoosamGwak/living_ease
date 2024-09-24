from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )

    def __str__(self):
        return self.nickname