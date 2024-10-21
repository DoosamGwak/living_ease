from django.urls import path
from . import views


app_name="pets"
urlpatterns = [
    path("questions/", views.QuestionListView.as_view()),
    path("recommands/", views.AIRecoomand.as_view()),
    path("metching-center/", views.MetchingCenter.as_view()),
    path("write/", views.AIAnserWrite.as_view()),
]