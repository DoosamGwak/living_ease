from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Board, Comment
from .serializers import (
    BoardListSerializer,
    BoardCreateSerializer,
    BoardDetailSerializer,
    CommentSerializer,
)


class BoardListAPIView(ListCreateAPIView):
    queryset = Board.objects.all().order_by("-id")
    serializer_class = BoardListSerializer

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BoardDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("이 게시글을 삭제할 권한이 없습니다.")
        instance.delete()


class CommentListAPIView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_object(self, pk):
        try:
            return Board.objects.get(pk=pk)
        except Board.DoesNotExist:
            raise NotFound("요청한 페이지가 없습니다")
    
    def perform_create(self, serializer):
        board_pk = self.kwargs.get("board_pk")
        board = self.get_object(pk=board_pk)

        comment_author = self.request.user

        serializer.save(board=board, user=comment_author)
        
        
class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
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
