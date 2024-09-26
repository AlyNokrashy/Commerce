from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add/", views.add_listing, name="add"),
    path("listing/<int:item_id>", views.listing, name="listing"),
    path(
        "categories/",
        views.categories,
        name="categories",
    ),
    path(
        "category/<int:category_id>/",
        views.category_listing,
        name="category_listing",
    ),
    path("remove/<int:item_id>", views.removeWatchlist, name="remove"),
    path("add/<int:item_id>", views.addWatchlist, name="add"),
    path("watchlist", views.wathclistDisplay, name="watchlist"),
    path("comment<int:item_id>", views.add_comment, name="comment"),
    path("bid<int:item_id>", views.add_bid, name="bid"),
    path("end_auction<int:item_id>", views.end_auction, name="end_auction"),
    path("bought_items", views.bought_items, name="bought_items"),
    path(
        "active_listings/<str:username>", views.active_listings, name="active_listings"
    ),
]
