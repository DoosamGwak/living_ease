from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path(
        "community/tip/",
        views.TipBoardListAPIView.as_view(),
        name="tip_list",
    ),
    path("community/walkingmate/", views.WalkingmateListAPIView.as_view(), name="walkingmate_list"),
    path("community/etc/", views.EtcListAPIView.as_view(), name="etc_list"),
    path("info/vaccine/",views.VaccineAPIView.as_view(),name="vaccine_list"),
    path("info/training/",views.TrainingAPIView.as_view(),name="training_list"),
    path("info/healthyfood/",views.HealthyfoodListAPIView.as_view(),name="healthyfood_list"),
    path("info/supplies/",views.SuppliesListAPIView.as_view(),name="supplies_list"),
    path("customer_service/notice/",views.SuppliesListAPIView.as_view(),name="supplies_list"),
    path("customer_service/faq/",views.FaqListAPIView.as_view(),name="faq_list"),
    path("customer_service/howtouse/",views.HowtouseListAPIView.as_view(),name="howtouse_list"),
    path("customer_service/directmsg/",views.DirectmsgListAPIView.as_view(),name="directmsg_list"),
    path("<int:board_pk>/", views.BoardDetailAPIView.as_view(), name="board_detail"),
    path(
        "<int:board_pk>/comments/",
        views.CommentListAPIView.as_view(),
        name="comment_list",
    ),
    path(
        "<int:board_pk>/comments/<int:comment_pk>/",
        views.CommentDetailAPIView.as_view(),
        name="comment_detail",
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
