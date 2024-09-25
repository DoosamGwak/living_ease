from django.urls import path
from . import views


app_name="pets"
urlpatterns = [
    path("questions/", views.QuestionListView.as_view()),
    path("recommands/", views.AIRecoomand.as_view()),
]