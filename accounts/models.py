from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20)
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    gender = models.CharField(choices=GENDER_CHOICES, null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    joined_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nickname