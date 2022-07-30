from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .forms import createFundraiserForm, donationForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from .models import *
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, "fundraiser/index.html",{
        "campaigns" : Campaign.objects.all().order_by('id').reverse()[0:3]
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
            return render(request, "fundraiser/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "fundraiser/login.html")


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
            return render(request, "fundraiser/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "fundraiser/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "fundraiser/register.html")

def create_fundraise(request):
    if request.method == "POST":
        form = createFundraiserForm(request.POST)
        try:
            new_campaign = form.save(commit=False)
            assert request.user.is_authenticated
            new_campaign.user = request.user
            new_campaign.save()
            return HttpResponseRedirect(reverse("index")) 
        except ValueError:
            pass
    else:
        form = createFundraiserForm()
    return render(request, "fundraiser/createfundraiser.html", {
        "form" : form
        })


def donate(request,campaign_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        campaign = Campaign.objects.get(id=campaign_id)
        donation_amount = request.POST.get("donation-amount")
        donation = Donation(donated_by=request.user, donated_for=campaign, donation=donation_amount)
        textarea = f'Thankyou for donating ${donation.donation} for "{campaign}"'
        confirm_msg = Message(user=request.user, sender=campaign.user, recipients=request.user, body=textarea, subject=campaign)
        confirm_msg.save()
        if int(donation_amount) >= 2 :
            donation.save()
            messages.success(request, 'Thank you for the Donation!')
        else: 
             messages.error(request, 'Minimum donation is $2')
        donation = Donation.objects.filter(donated_for=campaign_id)
        donation_count = donation.count()
        total = donation.aggregate(total_donation=Sum('donation'))
        
        return render(request, "fundraiser/fund.html", {
            "campaign" : campaign,
            "donation_count" : donation_count,
            "total" : total
        })
     
def campaign_details(request,campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    donation = Donation.objects.filter(donated_for=campaign_id)
    donation_count = donation.count()
    total = donation.aggregate(total_donation=Sum('donation'))
    today =  datetime.now().strftime('%b. %d, %Y')
    campaign.end_date = campaign.end_date.strftime('%b. %d, %Y')
    
    if request.method == "POST":
        assert request.user.is_authenticated
        textarea = request.POST["textarea"]
        message = Message(user=request.user, sender=request.user, recipients=campaign.user, body=textarea, subject=campaign)
        message.save()
    return render(request, "fundraiser/fund.html", {
        "campaign" : campaign,
        "donation_count" : donation_count,
        "total" : total,
        "today" : today
    }) 


def fund_list(request):
    campaigns = Campaign.objects.all().order_by('id').reverse()
    categories = Campaign.objects.values_list('category', flat=True)
    categories = list(set(categories))
    paginator = Paginator(campaigns, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "fundraiser/fundslist.html", {
        'page_obj': page_obj,
        "categories" : categories,
        "title" : f"All Campaigns"
    })    

def user_profile(request,user_id):
    profileuser = get_object_or_404(User, id=user_id)
    campaigns = Campaign.objects.filter(user=profileuser)
    donations = Donation.objects.filter(donated_by=profileuser)
    messages = Message.objects.filter(recipients=profileuser)
    return render(request, "fundraiser/profile.html", {
        "profileuser" : profileuser,
        "campaigns" : campaigns,
        "messages" : messages
    })


def category_list(request,category):
    page_obj = Campaign.objects.filter(category=category).order_by('id').reverse()
    categories = Campaign.objects.values_list('category', flat=True)
    categories = list(set(categories))
    return render(request, "fundraiser/fundslist.html", {
        "page_obj" : page_obj,
        "categories" : categories,
        "title": f'Campaigns in "{category}"'
    })

def add_comment(request,campaign_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        campaign = Campaign.objects.get(id=campaign_id)
        comment_content = request.POST['comment']
        comment = Comment(commenter=request.user, commented_on=campaign, comment=comment_content)
        comment.save()
        return HttpResponseRedirect(reverse("fund", args=(campaign_id,)))


@login_required
def myprofile(request,myprofile):
    if myprofile == "campaigns":
        works = Campaign.objects.filter(user=request.user)
    elif myprofile == "donations":
        works = Donation.objects.filter(donated_by=request.user)
    else:
        return JsonResponse({"error": "Invalid"}, status=400)

    works = works.order_by('-id').all()
    return JsonResponse([work.serialize() for work in works], safe=False)
    

@login_required
def chats(request, chats):
    if chats == "inbox":
        messages = Message.objects.filter(recipients=request.user)
    elif chats == "sent":
        messages = Message.objects.filter(sender=request.user, read=True)
    else:
        return JsonResponse({"error": "Inavalid"}, status=400)

    messages = messages.order_by('-id').all()
    return JsonResponse([message.serialize() for message in messages], safe=False)

@csrf_exempt
@login_required
def msg_detail(request, message_id,chats):
    if chats == "inbox":
        message = Message.objects.get(recipients=request.user, id=message_id)
    elif chats == "sent":
        message = Message.objects.get(sender=request.user, id=message_id)
    else:
        return JsonResponse({"error": "Message not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(message.serialize())

    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            message.read = data["read"]
        message.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "GET or PUT request required."}, status=400)
        
def close_campaign(request, campaign_id):
    if request.method == "POST":
        assert request.user.is_authenticated
        campaign = Campaign.objects.get(id=campaign_id)
        donation = Donation.objects.filter(donated_for=campaign_id)
        total = donation.aggregate(total_donation=Sum('donation'))
        if request.user == campaign.user :
            campaign.active = False
            campaign.save()
    return HttpResponseRedirect(reverse("fund", args=(campaign_id,)))
