from auctions.forms import  BidForm, CommentForm, NewListing
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import *
from django.core.exceptions import ValidationError

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
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

def listings(request, listing_id):
    bid = BidForm()
    comment_form = CommentForm()
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing_id)
    if request.method == "POST":
        bid = BidForm(request.POST)
        comment_form = CommentForm(request.POST)
        return render(request, "auctions/listings.html", {
            "listing": listing,
            "comments": comments,
            "message": "Must be higer than current price.",
            "bid_form": bid,
            "comment_form": comment_form
        })
    
    return render(request, "auctions/listings.html", {
        "listing": listing,
        "comments": comments,
        "bid_form": bid,
        "comment_form": comment_form
    })

@login_required
def new_listing(request):
    form = NewListing(request.POST)
    owner = request.user
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            start_bid = form.cleaned_data["start_bid"]
            img_url = form.cleaned_data["img_url"]
            category = form.cleaned_data["category"]
            if category == None:
               category = Category.objects.get(id=4) 
            listing = Listing(owner=owner, title=title, description=description,    start_bid=start_bid, img_url=img_url, category=category)
            listing.save()

        
        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/new_listing.html", {
        "form": form
    })

def watchlist(request):
    watchlist = request.user.watchlist
    populated = len(watchlist.all())
    
    return render(request, "auctions/watchlist.html", {
        "populated": populated,
        "watchlist": watchlist
    })
@login_required
def add_to_watchlist(request, listing_id): 
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    user.watchlist.add(listing.id)
    user.save()
    
    return HttpResponseRedirect(f"/auctions/{ listing.id }")

@login_required
def remove_from_watchlist(request, listing_id): 
    watchlist = request.user.watchlist
    listing = Listing.objects.get(id=listing_id)
    watchlist.remove(listing)
    
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def bids(request, listing_id):
    user = request.user
    bid_form = BidForm(request.POST)
    listing = Listing.objects.get(id=listing_id)
    if bid_form.is_valid():
        bid = bid_form.cleaned_data["bid"]
    if listing.high_bid == None:
        if float(bid) >= listing.start_bid:
            winning = Bid(listing=listing, user=user, bid=bid)
            listing.high_bid = winning
            listing.high_bid.save()
            listing.save()
            add_to_watchlist(request, listing_id=listing_id)

            return HttpResponseRedirect(f"/auctions/{ listing.id }")

        else:
            return listings(request, listing_id=listing.id)
        
    else: 
        if float(bid) > float(listing.high_bid.bid):
            winning = Bid(listing=listing, user=user, bid=bid)
            winning.save()
            listing.high_bid = winning
            listing.high_bid.save()
            listing.save()
            add_to_watchlist(request, listing_id=listing_id)

            return HttpResponseRedirect(f"/auctions/{ listing.id }")

        else:
            return listings(request, listing_id=listing.id)           

def close_listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing.active = False
    listing.save()

    return HttpResponseRedirect(f"/auctions/{ listing.id }")

@login_required
def add_comment(request, listing_id):
    user = request.user
    listing = Listing.objects.get(id=listing_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():       
        comment_txt = request.POST["comment_txt"]
    
    comment = Comment(user=user, listing=listing, content=comment_txt)
    comment.save()
    return HttpResponseRedirect(f"/auctions/{ listing.id }")

def categories_view(request):
    return render(request, "auctions/categories.html", {
        "categories":Category.objects.all()
    })

def category_filter(request, category_id):
    return render(request, "auctions/index.html", {
        "listings":Listing.objects.filter(category=category_id)
    })
'''
==============================================================
                        Up Next:
==============================================================
My items section
My purchases section
I could probably get rid of the Watchlist model if I give the User a watchlist attribute
Could do the same for the Category option if I wanted to learn about model.ChoiceField
Refactor HTML - listings and new_listings = Done
Reorder listings from new to old
Maybe add category.id to the filter_category view, then I can link straight to each page instead of using forms
Same for close_add, add_watchlist, remove_wathclist



https://stackoverflow.com/questions/63668493/django-how-to-use-validate-image-file-extension
'''
