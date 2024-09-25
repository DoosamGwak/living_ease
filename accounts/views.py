from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer, CustomTokenObtainPairSerializer,UserPofileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from rest_framework import status


class SignupView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "회원가입 완료"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "아이디나 비밀번호가 잘못되었습니다."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class UserProfileView(RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserPofileSerializer
    
    def get_object(self):
        return self.request.user


class UserUpdateView(UpdateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer   
