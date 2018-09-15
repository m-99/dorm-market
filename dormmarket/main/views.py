from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# first thing that user sees -> browse
def index(request):
    items = [
                {"image": "test.png", "name":"Fridge", "price":"50"},
                {"image": "test.png", "name":"Fridge 2", "price":"50"},
                {"image": "test.png", "name":"Fridge 2", "price":"50"},
                {"image": "test.png", "name":"Fridge 2", "price":"50"},
                {"image": "test.png", "name":"Fridge 2", "price":"50"},
                {"image": "test.png", "name":"Fridge 2", "price":"50"}
            ]
    rows = []
    for i in range(len(items)):
        if i % 3 == 0:
            rows.append([items[i]])
        else:
            rows[i//3].append(items[i])
    context = {
        "rows": rows
    }
    return render(request, 'main/index.html', context)

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

# show an item in detail
def focused(request):
    return HttpResponse("hey bb ur at focused")

# a form to submit a buy request for a type of item
def submit_buy(request):
    return HttpResponse("hey bb ur at submit_buy")

# a form to submit an item to be sold in the market
def submit_sell(request):
    return HttpResponse("hey bb ur at submit_sell")

# view items that you are selling in the marketplace
def sell_list(request):
    return HttpResponse("hey bb ur at sell_list")
