from django.shortcuts import get_object_or_404, render
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    UserPofileSerializer,
    UserDeleteSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth import authenticate


class SignupView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class CustomTokenObtainView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(
            {"error": "로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
        )


class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPofileSerializer


class UserDeleteView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer
    lookup_field = "username"

    # def get_object(self):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

    #     assert lookup_url_kwarg in self.kwargs, (
    #         self.__class__.__name__,
    #         lookup_url_kwarg,
    #     )

    #     filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
    #     obj = get_object_or_404(queryset, **filter_kwargs)
    #     obj.is_active = False

    #     self.check_object_permissions(self.request, obj)

    #     return obj
    def perform_update(self, serializer):
        serializer.save(is_active=False)
