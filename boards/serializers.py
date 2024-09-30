from rest_framework import serializers
from .models import Board, BoardImage, Comment
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
    images = BoardImageSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["title", "content", "username", "images"]

    def create(self, validated_data):
        images_data = self.context["request"].FILES
        board = Board.objects.create(**validated_data)
        for image_data in images_data.getlist("image"):
            BoardImage.objects.create(board=board, image=image_data)
        return board


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "username", "created_at", "updated_at"]
        read_only_fields = ["board"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret["user"] = instance.user.username
        return ret


class BoardDetailSerializer(IsAuthorValidator, serializers.ModelSerializer):
    images = BoardImageSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "content",
            "username",
            "comments_count",
            "comments",
            "images",
        ]

    def validate(self, data):
        request = self.context.get("request")
        self.validate_user(request.user, self.instance)
        return data
