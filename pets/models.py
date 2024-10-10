from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Question(models.Model):
    TYPE = [
        ("1", "TEXT"),
        ("2", "RANGE"),
        ("3", "RADIO"),
        ("4", "CHECK"),
    ]
    type = models.CharField(max_length=1, choices=[("1", "사용자"), ("2", "반려동물")])
    title = models.CharField(max_length=100)
    content = models.TextField()
    content_type = models.CharField(max_length=1, choices=TYPE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Choice(models.Model):
    QID = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.QID


class Answer(models.Model):
    QID = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="q_answers"
    )
    UID = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="u_answers"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.UID


class PetCategory(models.Model):
    type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class PetCode(models.Model):
    PCID = models.ForeignKey(
        PetCategory, on_delete=models.CASCADE, related_name="petcodes"
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AIHistory(models.Model):
    UID = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING, related_name="aihistorys"
    )
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.UID


class PetWikiImage(models.Model):
    PID = models.ForeignKey(
        PetCode, on_delete=models.DO_NOTHING, related_name="pet_images"
    )
    image = models.ImageField(upload_to="pets/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.PID
