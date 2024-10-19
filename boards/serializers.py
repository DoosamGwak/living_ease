from rest_framework import serializers
from django.db.models import QuerySet
from .models import Board, NoticeBoard, BoardImage, Comment, Category


class BoardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardImage
        fields = ["id", "image"]


class CommentSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "nickname", "created_at", "updated_at"]
        read_only_fields = ["board"]


# class BoardListSerializer(serializers.ModelSerializer):
#     nickname = serializers.CharField(source="user.nickname", read_only=True)
#     content_snippet = serializers.SerializerMethodField()

#     class Meta:
#         model = Board
#         fields = ["id", "title", "content_snippet", "nickname", "created_at"]

#     def get_content_snippet(self, obj):
#         specific_categories = ["vaccine", "training", " healthyfood", "supplies"]
#         if obj.category.name in specific_categories:
#             return " ".join(obj.content.split()[:30]) + "..." if obj.content else ""
#         return obj.content

class BoardListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)
    profile_image = serializers.ImageField(source="user.profile_image", read_only=True)
    content_snippet = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ["id", "title", "nickname", "profile_image", "content_snippet", "created_at", "comments", "content"]

    def get_fields(self):
        fields = super().get_fields()

        if isinstance(self.instance, list) or isinstance(self.instance, QuerySet):
            instance = self.instance[0] if self.instance else None
        else:
            instance = self.instance

        if instance:
            category_name = instance.category.name

            if category_name in ["walkingmate", "tip", "etc"]:
                # "nickname", "title", "created_at", "profile_image" 사용
                fields.pop("content_snippet")
                fields.pop("comments")
                fields.pop("content")  # content 필드 제거
            elif category_name in ["vaccine", "training", "healthyfood", "supplies"]:
                # "title", "content_snippet", "created_at" 사용
                fields.pop("nickname")
                fields.pop("profile_image")
                fields.pop("comments")
                fields.pop("content")  # content 필드 제거
            elif category_name in ["faq", "howtouse", "directmsg"]:
                # "title", "content", "created_at", "content" 사용
                fields.pop("nickname")
                fields.pop("profile_image")
                fields.pop("content_snippet")
                if category_name != "directmsg":
                    fields.pop("comments")

        return fields

    def get_content_snippet(self, obj):
        return " ".join(obj.content.split()[:20]) + "..." if obj.content else ""

    def get_comments(self, obj):
        if obj.category.name == "directmsg":
            return CommentSerializer(obj.comments.all(), many=True).data
        return None

class CommunityListSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "created_at", "nickname", "category_name"]


class NoticeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = NoticeBoard
        fields = ["id", "title", "content", "created_at"]


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


class CommunityCreateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(source="user.nickname", read_only=True)
    images = BoardImageSerializer(many=True, read_only=True)
    category = serializers.CharField()

    class Meta:
        model = Board
        fields = ["pk", "title", "content", "nickname", "images", "category"]

    def create(self, validated_data):
        images_data = self.context["request"].FILES
        category_name = validated_data.pop("category")
        try:
            category = Category.objects.get(
                name=category_name, parent__name="community"
            )
        except Category.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "해당 이름의 카테고리를 찾을 수 없습니다."}
            )
        validated_data["category"] = category

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
    images = BoardImageSerializer(source="board_images", many=True, read_only=True)
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
