from django.urls import path
from . import views

app_name="profiles"

urlpatterns = [
    path("/<str:username>/",views.ProfileDeytailView.as_view(),name="detail"),
    path("/<str:username>/follow",views.FollowView.as_view(),name="follow"),
    path("followers/",views.FollowerPage.as_view(),name="followers")
]
