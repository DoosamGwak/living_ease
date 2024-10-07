
from rest_framework import serializers
from .models import User
from .validators import CustomProfileDeleteValidator, OldPasswordValidator





class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["email", "password", "nickname", "name","age", "gender", "profile_image"]


class UserPofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "profile_image","nickname",  "age", "gender","joined_at"]


class UserDeleteSerializer(CustomProfileDeleteValidator, serializers.ModelSerializer):
    check_password = serializers.CharField(required=True,write_only=True)
    refresh = serializers.CharField(required=True, write_only =True)
    class Meta:
        model = User
        fields=["check_password", "refresh"]


class PasswordChangeSerializer(OldPasswordValidator,serializers.ModelSerializer):
    old_password = serializers.CharField(required=True,write_only=True)
    new_password = serializers.CharField(required=True,write_only=True)
    check_password = serializers.CharField(required=True,write_only=True)
    class Meta:
        model = User
        fields=["old_password","new_password","check_password"]
    
