from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import  *
from .forms import createListForm
from django.contrib import messages


def index(request):
    return render(request, "auctions/index.html", {
        "auctions" : Auction.objects.filter()
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing(request, auction_id):
    auctions = Auction.objects.get(pk=auction_id)
    if request.user.is_authenticated:
        is_watchlist = request.user.watchlist_item.filter(pk=auction_id).exists()
    else:
        is_watchlist = None
    return render(request, "auctions/listing.html", {
        "auction" : auctions,
        "is_watchlist" : is_watchlist,
    })

def newList(request):
    if request.method == "POST":
        form = createListForm(request.POST)
        try:
            new_list = form.save(commit=False)
            assert request.user.is_authenticated
            new_list.owner = request.user
            new_list.save()
            return HttpResponseRedirect(reverse("index"))
        except ValueError:
            pass

    else:
        form = createListForm()
        return render(request, "auctions/newList.html", {
            "form" : form
        })

def watchlist(request, auction_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        user = request.user
        auction = Auction.objects.get(pk=auction_id)
        is_watchlist = request.user.watchlist_item.filter(pk=auction_id).exists()
        if user.watchlist_item.filter(pk=auction_id).exists():
            user.watchlist_item.remove(auction)
        else:
            user.watchlist_item.add(auction)
    return HttpResponseRedirect(reverse("listing", args=(auction_id,)))

def watchlist_page(request):
    assert request.user.is_authenticated
    return render(request, "auctions/index.html", {
        "auctions" : request.user.watchlist_item.all(),
        "title" : "Watchlist Items"
    })

def categories(request):
    categories = Auction.objects.values_list('category', flat=True)
    categories = list(set(categories))
    return render(request, "auctions/category.html", {
        "categories" : categories
    })

def category_itemList(request, category):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(category=category),
        "title": f'Active listings in "{category}"'
    })

def add_comment(request,auction_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        auction = Auction.objects.get(pk=auction_id)
        comment_content = request.POST['comment']
        comment = Comment(commenter=request.user, commented_item=auction, comment=comment_content)
        comment.save()
        return HttpResponseRedirect(reverse("listing", args=(auction_id,)))

def bid_listing(request,auction_id):
    if request.method =="POST":
        assert request.user.is_authenticated
        auction = Auction.objects.get(pk=auction_id)
        bid_price = int(request.POST.get("bid_price"))
        starting_bid = int(auction.starting_bid)
        bid = Bid(user=request.user, bid_item=auction, bid_price=bid_price, listingid=auction_id)
        if bid_price <= starting_bid :
            auction = Auction.objects.get(id=auction_id)
            messages.warning(request, 'Your bid should be greater than current bid')
            return render(request, "auctions/listing.html", {
                "auction" : auction,
            })
        else:
            auction = Auction.objects.get(id=auction_id)
            bid.save()
            messages.success(request, 'Your bid is added')
            return render(request, "auctions/listing.html", {
                "auction" : auction,
            })
        return HttpResponseRedirect(reverse("listing", args=(auction_id,)))

def close_list(request, auction_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        auction = Auction.objects.get(id=auction_id)
        if request.user == auction.owner:
            auction.active = False
            auction.save()
    return HttpResponseRedirect(reverse("listing", args=(auction_id,))) 
        