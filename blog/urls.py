from django.urls import path
from . import views
urlpatterns = [
    path("" , views.IndexView.as_view() , name="index-page"),
    path("posts" , views.PostsView.as_view() , name="posts-page"),
    path("posts/<slug:slug>" , views.SingleView.as_view() , name="single") ,
    path("read-later" , views.ReadLaterView.as_view() , name="read-later"),
]
