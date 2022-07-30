from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_fundraise, name="create"),
    path("fund/<int:campaign_id>", views.campaign_details, name="fund"),
    path("donate/<int:campaign_id>", views.donate, name="donate"),
    path("funds", views.fund_list, name="fundlist"),
    path("profile/<int:user_id>", views.user_profile, name="profile"),
    path("funds/<str:category>", views.category_list, name="categoryfunds"),
    path("addcomment/<int:campaign_id>", views.add_comment, name="addComment"),
    path("close-fund/<int:campaign_id>", views.close_campaign, name="close"),

    # API
    path("profile/<str:myprofile>", views.myprofile, name="myprofile"),
    path("messages/<str:chats>", views.chats, name="chats"),
    path("messages/<str:chats>/<int:message_id>", views.msg_detail, name="msg_detail"),
    
]