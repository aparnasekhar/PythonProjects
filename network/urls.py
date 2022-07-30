
from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>/newpost", views.new_post, name="newpost"),
    path("profile/<str:username>", views.profile, name ="profile"),
    path("following/<str:username>", views.following, name="following"),
    path("posts/<int:post_id>/edit", views.edit_post, name="editpost"),
    url(r'^likepost/$', views.like_post, name='like-post')
]
