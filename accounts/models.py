from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    
    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=20,null=True,blank=True)
    name =models.CharField(max_length=15, blank=True)
    age = models.IntegerField(null=True,blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,  default="N",blank=True)
    profile_image = models.ImageField(
        upload_to="profile_images/", null=True, blank=True
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname