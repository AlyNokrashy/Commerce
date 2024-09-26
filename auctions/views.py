from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from decimal import Decimal


from .models import User, Category, Item, Bid, Comment


def index(request):
    active_listings = Item.objects.filter(activity=True)
    return render(request, "auctions/index.html", {"listings": active_listings})


@login_required
def add_listing(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST["title"].strip()
        description = request.POST["description"].strip()
        price = Decimal(request.POST["starting_bid"])
        category_id = request.POST["category"]
        category = Category.objects.get(id=category_id) if category_id else None
        img = request.POST["img"].strip()
        current_user = request.user
        bid = Bid(user=current_user, bid_amount=price)
        bid.save()

        new_item = Item(
            title=title,
            description=description,
            img=img,
            starting_bid=bid,
            user=current_user,
            category=category,
        )
        new_item.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/add.html", {"categories": categories})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def removeWatchlist(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    user = request.user
    item.watchlist.remove(user)
    messages.success(request, "Item removed from watchlist successfully!")
    return HttpResponseRedirect(reverse("listing", args=(item_id,)))


@login_required
def addWatchlist(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    user = request.user
    item.watchlist.add(user)
    messages.success(request, "Item added to watchlist successfully!")
    return HttpResponseRedirect(reverse("listing", args=(item_id,)))


@login_required
def wathclistDisplay(request):
    user = request.user
    item = user.watchlistItem.filter(activity=True)
    return render(request, "auctions/watchlist.html", {"listings": item})


def listing(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    isWatchlisted = request.user in item.watchlist.all()
    comments = Comment.objects.filter(item=item)
    is_item_owner = request.user.username == item.user.username
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": item,
            "isWatchlisted": isWatchlisted,
            "comments": comments,
            "is_item_owner": is_item_owner,
        },
    )


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def category_listing(request, category_id):
    category = Category.objects.filter(id=category_id).first()
    if not category:
        messages.error(request, "Category not found.")
    items = Item.objects.filter(category=category, activity=True)

    return render(
        request,
        "auctions/category_listing.html",
        {"category": category, "items": items},
    )


def add_comment(request, item_id):
    user = request.user
    item = Item.objects.filter(id=item_id).first()
    comment = request.POST["comment"]

    newComment = Comment(user=user, item=item, comment=comment)
    newComment.save()

    return HttpResponseRedirect(reverse("listing", args=(item_id,)))


def add_bid(request, item_id):
    user = request.user
    item = Item.objects.filter(id=item_id).first()
    bid = request.POST["bid"]
    bid_amount = Decimal(bid)
    current_bid_amount = item.starting_bid.bid_amount
    if bid_amount > current_bid_amount:
        newBid = Bid(user=user, bid_amount=bid_amount)
        newBid.save()
        item.starting_bid = newBid
        item.save()
        messages.success(request, "Your bid has been placed successfully!")
        return HttpResponseRedirect(reverse("listing", args=(item_id,)))

    messages.error(request, "Your bid must be higher than the current starting bid.")
    return HttpResponseRedirect(reverse("listing", args=(item_id,)))


def end_auction(request, item_id):
    item = Item.objects.filter(id=item_id).first()
    item.activity = False
    item.save()
    messages.success(request, "You ended your auction succesfully!")

    return HttpResponseRedirect(reverse("listing", args=(item_id,)))


def bought_items(request):
    user = request.user
    bought_items = Item.objects.filter(activity=False, starting_bid__user=user)
    return render(request, "auctions/bought.html", {"listings": bought_items})


def active_listings(request, username):
    user = User.objects.filter(username=username).first()
    active_items = Item.objects.filter(user=user, activity=True)
    return render(
        request,
        "auctions/active_listings.html",
        {"user": user, "listings": active_items},
    )
