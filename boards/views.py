from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Board, Comment, Category
from .permissions import IsStaffOrReadOnly
from .serializers import (
    BoardListSerializer,
    BoardCreateSerializer,
    BoardDetailSerializer,
    CommentSerializer,
)


def search_filter(queryset, search_word):
    if search_word:
        return queryset.filter(
            Q(title__icontains=search_word)
            | Q(content_icontains=search_word)
            | Q(user__username__icontains=search_word)
        )
    return queryset

def get_category(category_name):
    try:
        return Category.objects.get(name=category_name)
    except Category.DoesNotExist:
        raise NotFound("요청한 페이지가 없습니다.")


class TipListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        childcategory = get_category("tip")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        childcategory = get_category("tip")
        serializer.save(user=self.request.user, category=childcategory)


class WalkingmateListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        childcategory = get_category("walkingmate")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("walkingmate")
        serializer.save(user=self.request.user, category=category)


class EtcListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        childcategory = get_category("etc")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("etc")
        serializer.save(user=self.request.user, category=category)


class VaccineListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        childcategory = get_category("vaccine")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("vaccine")
        serializer.save(user=self.request.user, category=category)


class TrainingListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        childcategory = get_category("training")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("training")
        serializer.save(user=self.request.user, category=category)


class HealthyfoodListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        childcategory = get_category("healthyfood")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("healthyfood")
        serializer.save(user=self.request.user, category=category)


class SuppliesListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        childcategory = get_category("supplies")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("suppplies")
        serializer.save(user=self.request.user, category=category)


class NoticeListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        childcategory = get_category("notice")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("notice")
        serializer.save(user=self.request.user, category=category)


class FaqListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        childcategory = get_category("faq")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("faq")
        serializer.save(user=self.request.user, category=category)


class HowtouseListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        childcategory = get_category("howtouse")
        queryset=childcategory.boards.all().order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("howtouse")
        serializer.save(user=self.request.user, category=category)


class DirectmsgListAPIView(ListCreateAPIView):
    serializer_class = BoardListSerializer

    def get_queryset(self):
        childcategory = get_category("directmsg")
        queryset=childcategory.boards.filter(user=self.request.user).order_by("-id")
        search_word = self.request.query_params.get('search',None)
        return search_filter(queryset,search_word)
    

    def post(self, request, *args, **kwargs):
        self.serializer_class = BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        category = get_category("directmsg")
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
    serializer_class = CommentSerializer

    def get_queryset(self):
        board_pk = self.kwargs.get("board_pk")
        return Comment.objects.filter(board__pk=board_pk).order_by("-id")

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
    serializer_class = CommentSerializer
    lookup_field = "pk"

    def get_queryset(self):
        board_pk = self.kwargs.get("board_pk")
        return Comment.objects.filter(board__pk=board_pk)

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
