from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email", "username", "password", "nickname", "name","age", "gender", "profile_image"]
    
    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            name=validated_data["name"],
            nickname=validated_data["nickname"],
            email=validated_data["email"],
            gender=validated_data["gender"],
            age=validated_data["age"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        username = attrs.get("username")
        password = attrs.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("해당 유저네임은 없습니다.")

        return data

    def get_token(self, user):
        token = super().get_token(user)
        return token
    

class UserPofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "nickname", "email", "age", "gender","joined_at"]