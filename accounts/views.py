from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
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
    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        email = request.data.get("email")
        user = User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "email": user.email,
                "nickname": user.nickname,
                "pk":user.pk
            }
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        email = request.data.get("email")
        password = request.data.get("password")
        if not email or not password:
            raise ValidationError(
                {"detail": "이메일과 비밀번호를 모두 입력해야 합니다."}
            )
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"detail": "등록되지 않은 이메일입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(username=email, password=password)

        if user is None:
            return Response(
                {"detail": "이메일과 비밀번호를 다시 확인해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "email": user.email,
                "nickname": user.nickname,
                "pk":user.pk
            }
        )


class LogoutView(APIView):
    def post(self, request):
        data = request.data
        if not "refresh" in data:
            raise ValidationError({"detail": "refresh_token 값을 입력해주세요."})
        try:
            refresh_token = RefreshToken(data["refresh"])
            refresh_token.blacklist()
        except TokenError:
            raise ValidationError(
                {"detail": "refresh_token값이 유효하지 않습니다. 다시 입력해주세요"}
            )
        return Response(
            {"detail": "로그아웃에 성공하였습니다"}, status=status.HTTP_200_OK
        )


class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPofileSerializer
    lookup_field = "pk"

    def get_serializer(self, *args, **kwargs):
        kwargs["partial"] = True
        return super(UserProfileView, self).get_serializer(*args, **kwargs)

    def get_object(self):
        pk = self.kwargs.get(self.lookup_field)
        try:
            user = self.queryset.get(pk=pk)

            if not user.is_active:
                raise PermissionDenied({"detail": "탈퇴한 계정입니다."})

            return user
        except User.DoesNotExist:
            raise NotFound({"detail": "해당 닉네임의 사용자를 찾을 수 없습니다."})

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            raise PermissionDenied({"detail": "자신의 프로필만 수정할 수 있습니다."})
        return super().update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        serializer.save()


class UserDeleteView(UpdateAPIView):
    serializer_class = UserDeleteSerializer

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        user = self.get_object()
        if user != self.request.user:
            raise PermissionDenied({"detail": "권한이 없습니다"})
        serializer.save(is_active=False)
        user = serializer.save(is_active=False)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {"detail": "회원탈퇴에 성공하였습니다."}, status=status.HTTP_200_OK
        )


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordChangeSerializer

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data["old_password"]
            new_password = serializer.validated_data["new_password"]
            check_password = serializer.validated_data["check_password"]
            user = request.user
            if not user.check_password(old_password):
                return Response(
                    {"detail": "기존 비밀번호가 일치하지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if old_password == new_password:
                return Response(
                    {"detail": "기존의 비밀번호와 동일한 비밀번호입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if new_password != check_password:
                return Response(
                    {"detail": "새 비밀번호와 비밀번호 확인이 일치하지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(new_password)
            user.save()
            return Response(
                {"detail": "비밀번호가 변경되었습니다"}, status=status.HTTP_200_OK
            )
        return Response(
            {"detail": "비밀번호변경에 실패하였습니다"},
            status=status.HTTP_400_BAD_REQUEST,
        )
