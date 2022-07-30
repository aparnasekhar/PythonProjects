from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:auction_id>", views.listing, name="listing"),
    path("create", views.newList, name="create"),
    path("watchlist/<int:auction_id>", views.watchlist, name="watchlist"),
    path("watchlist", views.watchlist_page, name="watchlistpage"),
    path("category", views.categories, name="category"),
    path("category/<str:category>", views.category_itemList, name="categoryItems"),
    path("addcomment/<int:auction_id>", views.add_comment, name="addComment"),
    path("add-bid/<int:auction_id>", views.bid_listing, name="createBid"),
    path("close-list/<int:auction_id>", views.close_list, name="closeList")
]
