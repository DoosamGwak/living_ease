from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Question(models.Model):
    type = models.CharField(max_length=1, choices=[("1","사용자"), ("2","반려동물")])
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PetCategory(models.Model):
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PetCode(models.Model):
    PCID = models.ForeignKey(PetCategory, on_delete=models.CASCADE, related_name="petcodes")
    name=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AIHistory(models.Model):
    PID = models.ForeignKey(PetCode, related_name="petcodes")
    UID = models.ForeignKey(get_user_model, related_name="users")
    question = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)