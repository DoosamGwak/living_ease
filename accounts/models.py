from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = None
    last_name = None
    date_joined = None
    username = None

    GENDER_CHOICES = (("M", "Male"), ("F", "Female"))
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default="N", blank=True
    )

    profile_image = models.ImageField(
        upload_to="profile_images/",
        null=True,
        blank=True,
        default="profile_images/anonymous-user.webp",
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    objects = CustomUserManager()

    def __str__(self):
        return self.nickname
