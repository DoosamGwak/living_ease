from rest_framework import serializers
from .models import Board, BoardImage
from .validators import ImageValidator, IsAuthorValidator


class BoardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardImage
        fields = ["id", "image"]


class BoardListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "username"]


class BoardCreateSerializer(ImageValidator, serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    # child - 리스트 내의 객체들을 검증하는 데 사용될 필드 인스턴스. 이 인자가 제공되지 않으면 리스트 내의 객체들은 검증되지 않음
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Board
        fields = ["title", "content", "username", "images"]


class BoardDetailSerializer(IsAuthorValidator, serializers.ModelSerializer):
    images = BoardImageSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "content", "username", "images"]

    def validate(self, data):
        request = self.context.get("request")
        self.validate_user(request.user, self.instance)
        return data
