from django.urls import path
from . import views


urlpatterns = [
    path("", views.ChatbotView.as_view(), name="chatbot"),
    # path("pet/", views.PetbotView.as_view(), name="petbot"),
    # path("pet/ai/", views.PetAIInfoView.as_view(), name="petai")
]
