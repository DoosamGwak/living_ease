from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.exceptions import TokenError
from .models import User
from .serializers import (
    UserSerializer,
    UserPofileSerializer,
    UserDeleteSerializer,
    PasswordChangeSerializer,
)


class SignupView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            raise ValidationError("이메일과 비밀번호를 모두 입력해야 합니다.")
        user = authenticate(email=email, password=password)

        if user is not None:

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "email": user.email,
                    "nickname": user.nickname,
                }
            )
        return Response(
            {"error": "로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(APIView):
    def post(self, request):
        data = request.data
        if not "refresh" in data:
            raise ValidationError({"msg": "refresh_token 값을 입력해주세요."})
        try:
            refresh_token = RefreshToken(data["refresh"])
            refresh_token.blacklist()
        except TokenError:
            raise ValidationError(
                {"msg": "refresh_token값이 유효하지 않습니다. 다시 입력해주세요"}
            )
        return Response({"msg": "로그아웃에 성공하였습니다"}, status=status.HTTP_200_OK)


class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPofileSerializer
    lookup_field = "nickname"


class UserDeleteView(UpdateAPIView):
    serializer_class = UserDeleteSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = serializer.save(is_active=False)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordChangeSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.validated_data["new_password"]
            check_pasword = serializer.validated_data["check_password"]
            user = request.user
            if new_password == check_pasword:
                user.set_password(new_password)
                user.save()
                return Response(
                    {"msg": "비밀번호가 변경되었습니다"}, status=status.HTTP_200_OK
                )
            return Response(
                {"error": "비밀번호가 일치하지 않습니다"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"error": "비밀번호변경에 실패하였습니다"},
            status=status.HTTP_400_BAD_REQUEST,
        )
