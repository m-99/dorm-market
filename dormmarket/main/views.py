import json
import datetime
import time
from twilio.rest import Client

import requests
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json

from main.access_id import ACCESS_ID
from .forms import *
from .models import *

conditions = ['poor', 'okay', 'good', 'new', ]
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + ACCESS_ID,
}


# first thing that user sees -> browse
def index(request):
    items = Order.objects.order_by('-time_posted')[:9]
    rows = []
    for i in range(len(items)):
        if i % 3 == 0:
            rows.append([items[i]])
        else:
            rows[i // 3].append(items[i])
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
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def debug(request):
    if request.user.is_authenticated:
        user_object = User.objects.get(username=request.user.username)
        order = models.Order.objects.create(trader_name=user_object.profile,
                                            market_name="fridge",
                                            item_name="fridge huge drifdege",
                                            description="HUGE",
                                            image_url="https://brain-images-ssl.cdn.dixons.com/1/4/10174941/l_10174941_003.jpg",
                                            order_id="asdsd",
                                            time_posted="now")
        print(order.item_name)
        print(request.user.profile.order_set.all())
    else:
        print("Please Log in")
    return render(request, 'debug.html')


# show an item in detail
def focused(request):
    return HttpResponse("hey bb ur at focused")


# a form to submit a buy request for a type of item
def submit_buy(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            profile = request.user.profile
            user_object = User.objects.get(username=request.user.username)
            params = dict(request.POST)

            print(profile.order_set.all())

            order = models.Order.objects.create(trader_name=user_object.profile,
                                                item_name=params['item_name'],
                                                type=params['type'],
                                                image_url=params['image_url'])
            print(order)
            return redirect('index')
        else:
            print("Please Log in")
            return redirect('index')
    else:
        return HttpResponse("hey bb ur at submit_buy")


# a form to submit an item to be sold in the market
def submit_sell(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            profile = request.user.profile
            user_object = User.objects.get(username=request.user.username)
            params = dict(request.POST)

            print(profile.order_set.all())

            order = models.Order.objects.create(trader_name=user_object.profile,
                                                item_name=params['item_name'],
                                                type=params['type'],
                                                image_url=params['image_url'])
            print(order)
            return redirect('index')
        else:
            print("Please Log in")
            return redirect('index')
    else:
        return HttpResponse("hey bb ur at submit_sell")


# view items that you are selling in the marketplace
def trade_list(request):
    # if request.user.is_authenticated:
    #     profile = request.user.profile
    #     order_set = profile.order_set.all()

    #     print(order_set)
    #     # items = []
    #     # for order in order_set:
    #     #     items.append({"image": str(order.image_url),
    #     #                   "name": str(order.item_name),
    #     #                   "price": str(order.item_price)})
    #     items = order_set

    #     rows = []
    #     for i in range(len(items)):
    #         if i % 3 == 0:
    #             rows.append([items[i]])
    #         else:
    #             rows[i // 3].append(items[i])
    #     context = {
    #         "rows": rows
    #     }
    #     return render(request, 'trade_list.html', context)
    # else:
    #     print("Please Log in")
    #     return render(request, 'trade_list.html')
    return render(request, 'user_info.html')


def sell(request):
    if request.method == 'POST':
        # get the form info
        market = request.POST['market']
        condition = request.POST['condition']
        description = request.POST['description']
        price = int(request.POST['price'])
        quantity = 1

<<<<<<< HEAD
        user_id = 'luke_test_user_id'
=======
		user_id = 'luke_test_user_id'



>>>>>>> updated urls to not use regex where unnecessary; further developed

        r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={},
                         headers=headers)

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
                },
            })

            # Creates the market
            r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/',
                              params=params, data=body, headers=headers)

            print(r.json())
            market_id = r.json()['data']

            print(conditions)

            # Make new assets for each condition
            for condition in conditions:
                body = json.dumps({
                    "assetName": condition + ' ' + market,
                    "attributes": {
                        "condition": condition
                    },
                })

                # POST new asset
                r = requests.post(
                    'http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/%s/' % (market_id,),
                    params={}, data=body, headers=headers)

<<<<<<< HEAD
            # Get new markets
            r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/',
                             params={}, headers=headers)
=======
			# Get new markets
			r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={}, headers = headers)

		# Map market names to IDS
		markets = {market['marketName']: market['marketId'] for market in r.json()['data']}

		# Get market ID
		market_id = markets[market]
>>>>>>> updated urls to not use regex where unnecessary; further developed

        # Map market names to IDS
        markets = {market['marketName']: market['marketId'] for market in r.json()['data']}

        # Get market ID
        market_id = markets[market]

        print('MARKET ID', market_id)

        # Get asset for correct condition
        r = requests.get(
            'http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/get_assets/%s/' % (
                market_id,), params={
                "queries": ['"condition" = \'' + condition + '\'']
            }, headers=headers)

        print('ASSETS:', r.json())

        asset_id = r.json()['data'][0]

<<<<<<< HEAD
        print('ASSET_ID:', asset_id)
=======
		# Post new listing
		params = {
			'assetId': asset_id,
		}

		body = json.dumps({
			'price': price,
			'qty': quantity,
			'userId': user_id,
		})
>>>>>>> updated urls to not use regex where unnecessary; further developed

        # Post new listing
        params = {
            'assetId': asset_id,
        }

        body = json.dumps({
            'price': price,
            'qty': quantity,
            'userId': user_id,
        })

        r = requests.post(
            'http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/asks/%s/' % (market_id,),
            params=params, data=body, headers=headers)

    # Return a redirect to your post

    else:
        form = SellForm()
        return render(request, 'main/sell.html', {'form': form})

<<<<<<< HEAD

def buy(request):
    if request.method == 'POST':
        # get the form info
        market = request.POST['market']
        condition = request.POST['condition']
        description = request.POST['description']
        price = int(request.POST['price'])
        quantity = 1

        user_id = 'luke_test_user_id_buy'

        # Get markets
        r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={},
                         headers=headers)

        print(r.json()['data'])

        # Check that a market exists
        if market not in [market['marketName'] for market in r.json()['data']]:
            # Market doesn't exist
            print('market not found')
            return None

        # Map market names to IDS
        markets = {market['marketName']: market['marketId'] for market in r.json()['data']}

        # Get market ID
        market_id = markets[market]

        print('MARKET ID', market_id)

        # Get asset for correct condition
        # Make a BUY request for every condition <= condition
        cond_id = conditions.index(condition)
        for i in range(cond_id, len(conditions)):
            r = requests.get(
                'http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/get_assets/%s/' % (
                    market_id,), params={
                    "queries": ['"condition" = \'' + conditions[i] + '\'']
                }, headers=headers)

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

            r = requests.post(
                'http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/bids/%s/' % (market_id,),
                params=params, data=body, headers=headers)

    # Return a redirect to your buys

    else:
        form = BuyForm()
        return render(request, 'main/buy.html', {'form': form})


def get_order_book(request):
    if True or request.method == 'POST':
        side = 'bids'
        params = {

        }

        try:
            check_order_filled(request)
            r = requests.get(
                'http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/' + side + '/',
                params=params, headers=headers)
            print(r)
            info = r.json()['data']
            print(info)
            print(len(info))
            print()
            print(len(info[0]))
        except Exception as e:
            print("Request to API failed: " + e)

        return render(request, 'main/view_market.html')
    else:
        return render(request, 'main/view_market.html')


def check_order_filled(request):
    try:
        profile = request.user.profile
        order_set = profile.order_set.all()

        r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/transactions/',
                         params={}, headers=headers)
        print("trades: ", r)
        print("trades: ", r.json())
        info = r.json()['data']
        print(info)
        for order in info:
            if order['timestamp'] > time.time() * 1000 - 30000:
                if str(order_set.order_id) in (order['askId'], order['bidId']):
                    send_notification()
                    return True

    except Exception as e:
        print("Request to API failed: " + e)

    return False


def send_notification():
    # Your Account Sid and Auth Token from twilio.com/console
    account_sid = 'AC6dd084097904f1cf92ad8bc2b358fa87'
    auth_token = '113f188d5e893c3b3abaea5e6a0ccd40'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Your order was successfully processed as of " + str(datetime.datetime.now()),
        from_='+16176185707',
        to='+16173350541'
    )

    print(message.sid)
=======

	else:
		form = SellForm()
		return render(request, 'main/sell.html', {'form': form})

def buy(request):
	if request.method == 'POST':
		# get the form info
		market = request.POST['market']
		condition = request.POST['condition']
		description = request.POST['description']
		price = int(request.POST['price'])
		quantity = 1

		user_id = 'luke_test_user_id_buy'



		# Get markets
		r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={}, headers = headers)

		print(r.json()['data'])

		# Check that a market exists
		if market not in [market['marketName'] for market in r.json()['data']]:
			# Market doesn't exist
			print('market not found')
			return None

		# Map market names to IDS
		markets = {market['marketName']: market['marketId'] for market in r.json()['data']}

		# Get market ID
		market_id = markets[market]

		print('MARKET ID', market_id)

		# Get asset for correct condition
		# Make a BUY request for every condition <= condition
		cond_id = conditions.index(condition)
		for i in range(cond_id, len(conditions)):

			r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/get_assets/%s/' % (market_id,), params={
				"queries": ['"condition" = \'' + conditions[i] + '\'']
			}, headers = headers)

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

			r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/bids/%s/' % (market_id,), params = params, data=body, headers = headers)

		# Return a redirect to your buys



	else:
		form = BuyForm()
		return render(request, 'main/buy.html', {'form': form})
>>>>>>> updated urls to not use regex where unnecessary; further developed
