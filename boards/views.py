from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Board
from .serializers import BoardSerializer,BoardCreateSerializer, BoardDetailSerializer

class BoardListAPIView(ListCreateAPIView):
    queryset=Board.objects.all()
    serializer_class=BoardSerializer
    
    
    def post(self, request, *args, **kwargs):
        self.serializer_class=BoardCreateSerializer
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class BoardDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset=Board.objects.all()
    serializer_class=BoardDetailSerializer
    
    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("이 게시글을 삭제할 권한이 없습니다.")
        instance.delete()