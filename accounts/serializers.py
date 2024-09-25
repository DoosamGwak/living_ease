from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["email", "username", "password", "nickname", "name","age", "gender", "profile_image"]



class UserPofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "name", "email", "profile_image","nickname",  "age", "gender","joined_at"]

class UserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=["password","nickname",]