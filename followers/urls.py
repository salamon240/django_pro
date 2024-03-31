from django.urls import path
from . import views

app_name="follower"

urlpatterns = [
    path("/<str:username>/",views.ProfileDeytailView.as_view(),name="detail"),
    path("/<str:username>/follow",views.FollowView.as_view(),name="follow")
]
