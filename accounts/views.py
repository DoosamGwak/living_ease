from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


class SignupView(CreateAPIView):
    permission_classes=[AllowAny]
    pass
