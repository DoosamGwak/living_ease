from django.contrib import admin
from .models import Category, Board, NoticeBoard, BoardImage


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(NoticeBoard)
class NoticeBoardAdmin(admin.ModelAdmin):
    pass


@admin.register(BoardImage)
class BoardImageAdmin(admin.ModelAdmin):
    pass
