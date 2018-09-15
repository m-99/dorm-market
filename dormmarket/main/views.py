from django.http import HttpResponse
from django.shortcuts import render
<<<<<<< dc79ebffe3d9dbdf55ff64b0ddd1a513bfbe09e0
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . import models
=======
from main.access_id import ACCESS_ID
import requests
from .forms import SellForm
import json

conditions = ['poor', 'okay', 'good', 'new']
headers = {
		  'Content-Type': 'application/json',
		  'Accept': 'application/json',
		  'Authorization': 'Bearer ' + ACCESS_ID,
		}

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

def sell(request):
	if request.method == 'POST':
		# get the form info
		market = request.POST['market']
		condition = request.POST['condition']
		#tags = request.POST['tags']
		description = request.POST['description']
		price = int(request.POST['price'])
		quantity = 1

		user_id = 'luke_test_user_id'
		
		
		

		r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={}, headers = headers)

		print(r.json()['data'])

		# Check that a market exists
		if market not in [market['marketName'] for market in r.json()['data']]:
			# Create the market if it doesn't
			params = {
			}

			body = json.dumps({
					'name': market,
					'attributes': {
						'condition': 'text',
						'description': 'text',
					},
				})

			# Creates the market
			r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params = params, data=body, headers = headers)

			print(r.json())
			market_id = r.json()['data']

			# Make new assets for each condition
			for condition in conditions:
				body = json.dumps({
					"assetName": condition + market,
					"attributes": {
						"condition": condition
					},
				})

				# POST new asset
				r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/%s/' % (market_id,), params = {}, data=body, headers = headers)

			# Get new markets
			r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={}, headers = headers)
		
		# Map market names to IDS
		markets = {market['marketName']: market['marketId'] for market in r.json()['data']}
		
		market_id = markets[market]

		print('MARKET ID', market_id)

		# Get asset for correct condition
		r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/get_assets/%s/' % (market_id,), params={
			"queries": ['"condition" = \'' + condition + '\'']
		}, headers = headers)

		print('ASSETS:', r.json())

		asset_id = r.json()['data'][0]

		print('ASSET_ID:', asset_id)


		# Post new listing
		params = {
			'assetId': asset_id,
		}
		
		body = json.dumps({
			'price': price,
			'qty': quantity,
			'userId': user_id,
		})

		r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/asks/%s/' % (market_id,), params = params, data=body, headers = headers)

		# Return a redirect to your post


	
	else:
		form = SellForm()
		return render(request, 'main/sell.html', {'form': form})
