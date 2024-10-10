from rest_framework import serializers
from .models import User
from .validators import (
    CustomProfileDeleteValidator,
    OldPasswordValidator,
    PasswordValidator,
)


class UserSerializer(serializers.ModelSerializer, PasswordValidator):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password2",
            "nickname",
            "name",
            "age",
            "gender",
            "profile_image",
        ]

    def validate(self, attrs):
        self.validate_password_check(attrs["password"], attrs["password2"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class UserPofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "profile_image",
            "nickname",
            "age",
            "gender",
            "joined_at",
        ]


class UserDeleteSerializer(CustomProfileDeleteValidator, serializers.ModelSerializer):
    check_password = serializers.CharField(required=True, write_only=True)
    refresh = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["check_password", "refresh"]


class PasswordChangeSerializer(OldPasswordValidator, serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    check_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["old_password", "new_password", "check_password"]
