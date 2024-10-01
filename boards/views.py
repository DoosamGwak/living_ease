from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Board, Comment, Category
from .serializers import (
    BoardListSerializer,
    BoardCreateSerializer,
    BoardDetailSerializer,
    CommentSerializer,
)


def get_category(category_name):
    try:
        return Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        raise NotFound("요청한 페이지가 없습니다.")


class CommunityBoardListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        category = get_category("community")
        return Board.objects.filter(category=category).order_by("-id")

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("community")
        serializer.save(user=self.request.user, category=category)


class TipBoardListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        category = get_category("tip")
        return Board.objects.filter(category=category).order_by("-id")

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("tip")
        serializer.save(user=self.request.user, category=category)


class NoticeBoardListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        category = get_category("notice")
        return Board.objects.filter(category=category).order_by("-id")

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("notice")
        serializer.save(user=self.request.user, category=category)


class BoardDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    lookup_field = "pk"

    def get_object(self):
        board_pk = self.kwargs.get("board_pk")
        try:
            return Board.objects.get(pk=board_pk)
        except Board.DoesNotExist:
            raise NotFound("요청한 게시글이 없습니다.")

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("이 게시글을 수정할 권한이 없습니다.")

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("이 게시글을 삭제할 권한이 없습니다.")
        instance.delete()


class CommentListAPIView(ListCreateAPIView):
    queryset = Comment.objects.all().order_by("-id")
    serializer_class = CommentSerializer

    def get_object(self):
        board_pk = self.kwargs.get("board_pk")
        try:
            return Board.objects.get(pk=board_pk)
        except Board.DoesNotExist:
            raise NotFound("요청한 게시글이 없습니다")

    def perform_create(self, serializer):
        board_pk = self.kwargs.get("board_pk")
        board = self.get_object(pk=board_pk)
        comment_author = self.request.user
        serializer.save(board=board, user=comment_author)


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"

    def get_object(self):
        comment_pk = self.kwargs.get("comment_pk")
        try:
            return Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            raise NotFound("요청한 댓글이 없습니다.")

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("이 댓글을 수정할 권한이 없습니다.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("이 댓글을 삭제할 권한이 없습니다.")
        instance.delete()
