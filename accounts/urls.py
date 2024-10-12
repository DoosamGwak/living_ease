from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path(
        "profile/<str:nickname>/", views.UserProfileView.as_view(), name="user_profile"
    ),
    path("password/", views.ChangePasswordView.as_view(), name="change_password"),
    path("delete/", views.UserDeleteView.as_view(), name="user_delete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
