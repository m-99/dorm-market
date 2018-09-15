from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . import models

# first thing that user sees -> browse
def index(request):

    return HttpResponse("hey bb ur at the main index")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('')
    else:
        form = UserCreationForm()
    return render(request, 'templates/signup.html', {'form': form})

def debug(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        order = models.Order.objects.create(trader_name=user_object.profile, item_name="<item_name>", type="b",
                             image_url="https://brain-images-ssl.cdn.dixons.com/1/4/10174941/l_10174941_003.jpg")
        print(order.item_name)
        print(request.user.profile.order_set.all())
    else:
        print("Please Log in")
    return render(request, 'templates/debug.html')

# show an item in detail
def focused(request):
    return HttpResponse("hey bb ur at focused")


# a form to submit a buy request for a type of item
def submit_buy(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            profile = request.user.profile
            user_object = User.objects.get(username=request.user.username)
            print(request.POST)
            print(profile)
            print(profile.order_set.all())

            order = models.Order.objects.create(trader_name=user_object.profile, item_name="<item_name>", type="b",
                             image_url="https://brain-images-ssl.cdn.dixons.com/1/4/10174941/l_10174941_003.jpg")
            print(order)
            return redirect('')
        else:
            print("Please Log in")
            return redirect('')
    else:
        pass
    return HttpResponse("hey bb ur at submit_buy")


# a form to submit an item to be sold in the market
def submit_sell(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            print(request.POST)
            print(request.user.profile)
            print(request.user.profile.order_set.all())
            return redirect('')
        else:
            print("Please Log in")
            return redirect('')
    else:
        pass
    return HttpResponse("hey bb ur at submit_sell")


# view items that you are selling in the marketplace
def sell_list(request):
    return HttpResponse("hey bb ur at sell_list")
