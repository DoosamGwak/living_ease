from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.BoardListAPIView.as_view(), name="board_list"),
    path("<int:board_pk>/", views.BoardDetailAPIView.as_view(), name="board_detail"),
    path("<int:board_pk>/comments/", views.CommentListAPIView.as_view(), name="comment_list"),
    path(
        "comments/<int:comment_pk>/",
        views.CommentDetailAPIView.as_view(),
        name="comment_detail",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
