from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework_simplejwt.views import TokenRefreshView




urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/",views.CustomTokenObtainView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("<str:username>/",views.UserProfileView.as_view()),
    path("<str:username>/",views.UserUpdateView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
