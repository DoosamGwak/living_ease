
from rest_framework import serializers
from .models import User
from .validators import CustomProfileDeleteValidator


class UserSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = User
        fields = ["email", "username", "password", "nickname", "name","age", "gender", "profile_image"]


class UserPofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "email", "profile_image","nickname",  "age", "gender","joined_at"]


class UserDeleteSerializer(CustomProfileDeleteValidator, serializers.ModelSerializer):
    check_password = serializers.CharField(required=True,write_only=True)
    refresh = serializers.CharField(required=True, write_only =True)
    class Meta:
        model = User
        fields=["check_password", "refresh"]

