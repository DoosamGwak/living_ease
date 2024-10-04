from django.db import models
from accounts.models import User


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="childcategories",
    )

    def __str__(self):
        return self.name


class Board(TimeStampedModel):
    title = models.CharField(max_length=30)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="boards")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="boards"
    )

    def __str__(self):
        return self.title


class BoardImage(TimeStampedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="boards/", null=True, blank=True)

    def __str__(self):
        return f"Image for {self.board.title}"
    
    
class NoticeBoard(Board):
    priority = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"[우선순위 {self.priority}] {self.title}"


class Comment(TimeStampedModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
