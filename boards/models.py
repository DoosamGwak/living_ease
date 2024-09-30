from django.db import models
from accounts.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Board(TimeStampedModel):
    title = models.CharField(max_length=30)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards")

    def __str__(self):
        return self.title


class BoardImage(TimeStampedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="boards/", null=True, blank=True)

    def __str__(self):
        return f"Image for {self.board.title}"


class Comment(TimeStampedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
