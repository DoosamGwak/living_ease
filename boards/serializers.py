from rest_framework import serializers
from .models import Board, NoticeBoard, BoardImage, Comment, Category


class BoardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardImage
        fields = ["id", "image"]


class BoardListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = NoticeBoard
        fields = ["id", "title", "nickname"]
        

class NoticeListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = NoticeBoard
        fields = ["id", "title", "nickname"]


class BoardCreateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)
    images = BoardImageSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["title", "content", "nickname", "images"]

    def create(self, validated_data):
        images_data = self.context["request"].FILES
        board = Board.objects.create(**validated_data)
        for image_data in images_data.getlist("image"):
            BoardImage.objects.create(board=board, image=image_data)
        return board


class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "nickname", "created_at", "updated_at"]
        read_only_fields = ["board"]


class BoardDetailSerializer(serializers.ModelSerializer):
    images = BoardImageSerializer(many=True, read_only=True)
    nickname = serializers.CharField(source="user.nickname", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "content",
            "nickname",
            "comments_count",
            "comments",
            "images",
            "category",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if (
            instance.category.parent
            and instance.category.parent.name == "customer_service"
        ):
            data.pop("comments", None)
            data.pop("comments_count", None)
        return data


class NoticeCreateSerializer(BoardCreateSerializer):
    priority = serializers.IntegerField(default=1)
    class Meta(BoardCreateSerializer.Meta):
        model = NoticeBoard
        fields = BoardCreateSerializer.Meta.fields + ["priority"]

    def create(self, validated_data):
        priority = validated_data.pop("priority", 1)
        notice_board = NoticeBoard.objects.create(**validated_data, priority=priority)
        images_data = self.context["request"].FILES
        for image_data in images_data.getlist("image"):
            BoardImage.objects.create(board=notice_board, image=image_data)

        return notice_board


class NoticeDetailSerializer(BoardDetailSerializer):
    priority = serializers.IntegerField(read_only=True)

    class Meta(BoardDetailSerializer.Meta):
        model = NoticeBoard
        fields = BoardDetailSerializer.Meta.fields + ["priority"]
        fields.remove("comments")
        fields.remove("comments_count")


class CategorySerializer(serializers.ModelSerializer):
    boards = BoardListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "boards"]
