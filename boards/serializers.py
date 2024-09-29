from rest_framework import serializers
from .models import Board, BoardImage

class BoardImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardImage
        fields = ['id', 'image']

class BoardSerializer(serializers.ModelSerializer):
    images = BoardImageSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title', 'content', 'user', 'images',]

class BoardCreateSerializer(serializers.ModelSerializer):
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