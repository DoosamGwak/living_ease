from rest_framework import serializers
from .models import Board, BoardImage
from .validators import ImageValidator, IsAuthorValidator

class BoardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardImage
        fields = ['id', 'image']

class BoardSerializer(serializers.ModelSerializer):
    images = BoardImageSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'username', 'images',]

class BoardCreateSerializer(ImageValidator, serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    #child - 리스트 내의 객체들을 검증하는 데 사용될 필드 인스턴스. 이 인자가 제공되지 않으면 리스트 내의 객체들은 검증되지 않음
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Board
        fields = ['title', 'content', 'user', 'images']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        board = Board.objects.create(**validated_data)

        for image in images:
            BoardImage.objects.create(board=board, image=image)

        return board
    

class BoardDetailSerializer(IsAuthorValidator, serializers.ModelSerializer):
    images = BoardImageSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'username', 'images']
    
    def validate(self, data):
        # 요청 유저(request.user)와 게시글 작성자가 동일한지 검증
        request = self.context.get('request')  # context에서 request 객체를 가져옴
        self.validate_user(request.user, self.instance)  # 검증 로직 호출
        return data