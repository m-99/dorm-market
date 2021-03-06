import datetime
import json
import requests
import datetime
import time
from twilio.rest import Client

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from main.access_id import ACCESS_ID
from django.urls import reverse

from .forms import *
from .models import *
from . import models
from . import mail

conditions = ['poor', 'okay', 'good', 'new', ]
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer ' + ACCESS_ID,
}

def callAPI(api_path, params):
    while True:
        try:
            r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/'+api_path, params=params, headers = headers, timeout = 0.1)
            return r.json()
            break
        except:
            pass

def asset_exists_for_market(market, market_assets):
    # print(market[0])
    # print(market_assets)
    if market_assets[market[0]]['poor'] > 0:
        return True
    elif market_assets[market[0]]['okay'] > 0:
        return True
    elif market_assets[market[0]]['good'] > 0:
        return True
    elif market_assets[market[0]]['new'] > 0:
        return True

    return False

# first thing that user sees -> browse
def index(request):

    # loads all market ids
    unique_markets = []
    market_objects = []
    market_ids = {}
    data = callAPI("markets/", {})['data']
    for market_obj in data:
        market_ids[market_obj['marketName']] = market_obj['marketId']
        unique_markets.append(market_obj['marketName'])
        filtered_orders = Order.objects.filter(market_name = market_obj['marketName'])
        imgurl = "test.png"
        if len(filtered_orders) > 0:
            imgurl = filtered_orders[0].image.url
        market_objects.append([market_obj['marketName'], imgurl])

    # for each market, find all asset ids
    market_asset_ids = {}
    for market in unique_markets:
        asset_ids = callAPI('assets/get_assets/'+market_ids[market]+'/', {})['data']
        market_asset_ids[market] = asset_ids

    # loads asset information for each market
    market_assets = {}
    orders_response = callAPI('orders/asks/', {})['data']
    orders = {}
    for order in orders_response:
        if order['assetId'] in orders:
            orders[order['assetId']].append(order['orderId'])
        else:
            orders[order['assetId']] = [order['orderId']]
    print(orders)
    for market in unique_markets:
        asset_objects = callAPI('assets/get_assets_by_ids/'+market_ids[market]+'/', {'assetId': market_asset_ids[market]})['data']
        assets = {}
        for asset in asset_objects:
            # Get best price
            condition = False
            r = callAPI("orders/asks/lowest_ask", {'assetId': asset['assetId']})
            try:
                price = int(r['data'][0]['price'])
            except:
                price = 0
            assets[asset['assetName']] = price

            # print("ASSET ID "+str(asset['assetId']))
            
            assets[asset['assetName']+"_img"] = "test.png"
            if asset['assetId'] in orders:
                print(orders[asset['assetId']])
                filtered_orders = Order.objects.filter(market_name = market)
                print(filtered_orders)
                if len(filtered_orders) > 0:
                    url = filtered_orders[0].image.url
                    assets[asset['assetName']+"_img"] = url
        market_assets[market] = assets


    # organizes markets to display into rows
    rows = []
    items_added = 0
    for i in range(len(market_objects)):
        if asset_exists_for_market(market_objects[i], market_assets) == True:
            if i % 3 == 0:
                rows.append([market_objects[i]])
            else:
                rows[items_added // 3].append(market_objects[i])
            items_added += 1
    context = {
        "rows": rows,
        "markets": market_objects,
        "assets": market_assets
    }
    return render(request, 'main/index.html', context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            print(request.POST)
            user.profile.phone_number = request.POST['phone_number']
            user.profile.email = request.POST['email']
            user.profile.save()
            user.save()
            print(dir(user))
            return redirect('index')
    else:
        form = SignUpForm()
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


# view items that you are selling in the marketplace
def trade_list(request):
    # get all orders associated with user
    user_orders = request.user.profile.order_set.all()
    sell_orders = user_orders.exclude(description="").filter(notified="N")  # .sort_by('-time_posted')
    buy_orders = user_orders.filter(description="").filter(notified="N")  # .sort_by('-time_posted')

    print(sell_orders)
    print(buy_orders)

    user_order_ids = []
    for order in user_orders:
        user_order_ids.append(order.order_id)

    # We're pretty sure that /orders/{asks/bids} doesn't work
    # while True:
    #     try:
    #         print(user_order_ids)
    #         r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/asks', params={}, headers = headers, timeout = 0.1)
    #         # order objects in data
    #         data = r.json()['data']
    #         break
    #     except:
    #         pass

    # prices = {}

    context = {'buy_orders': buy_orders,
               'sell_orders': sell_orders}

    return render(request, 'user_info.html', context)


def sell(request):
    # Get all markets
    while True:
        try:
            r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={}, headers = headers, timeout=0.1)
            break
        except:
            pass

    markets = r.json()['data']

    if request.method == 'POST':
        # get the form info
        if request.POST['market_name'] == 'other':
            market = request.POST['market-other']
        else:
            market = request.POST['market_name']
        condition = request.POST['condition']
        description = request.POST['description']
        price = int(request.POST['price'])
        quantity = 1

        user_id = str(request.user.pk)

        # Check that a market exists
        if market not in [market['marketName'] for market in markets]:
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
            while True:
                try:
                    r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params = params, data=body, headers = headers, timeout=0.1)
                    break
                except:
                    pass

            #print(r.json())
            market_id = r.json()['data']

            #print(conditions)

            # Make new assets for each condition
            for condition in conditions:
                body = json.dumps({
                    "assetName": condition,
                    "attributes": {
                        "condition": condition
                    },
                })

                # POST new asset
                while True:
                    try:
                        r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/%s/' % (market_id,), params = {}, data=body, headers = headers, timeout=0.1)
                        break
                    except:
                        pass

            # Get new markets
            while True:
                try:
                    r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={}, headers = headers, timeout=0.1)
                    break
                except:
                    pass

        # Map market names to IDS
        markets = {market['marketName']: market['marketId'] for market in r.json()['data']}

        # Get market ID
        market_id = markets[market]

        # print('MARKET ID', market_id)

        # Get asset for correct condition
        while True:
            try:
                r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/get_assets/%s/' % (market_id,), params={
                    "queries": ['"assetName" = \'' + condition + '\'']
                }, headers = headers, timeout = 0.1)
                break
            except:
                pass

        # print('ASSETS:', r.json())

        asset_id = r.json()['data'][0]

        # print('ASSET_ID:', asset_id)

        # Post new listing
        params = {
            'assetId': asset_id,
        }

        body = json.dumps({
            'price': price,
            'qty': quantity,
            'userId': user_id,
        })

        while True:
            try:
                r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/asks/%s/' % (market_id,), params = params, data=body, headers = headers, timeout = 0.1)
                break
            except:
                pass

        # Make an Order object linked to the user
        print('ASK:', r.json())
        '''
        if r.json()['message'] != 'Order filled!':
            order_id = r.json()['data']['order']['_id']
        else:
            '''
        order_id = r.json()['data']['order']['orderId']

        form = SellForm({'description': description, 'market_name': market, "order_id": order_id}, request.FILES)
        if form.is_valid():
            order = form.save(commit = False)
            order.trader_name = request.user.profile
            order.save()
            check_order_filled(request)
            return HttpResponseRedirect(reverse('index'))
        else:
            print('form not valid')


    else:
        context = dict()
        context['markets'] = markets
        return render(request, 'main/sell_new.html', context)

def buy(request):

    # Get all markets
    while True:
        try:
            r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={}, headers = headers, timeout=0.1)
            break
        except:
            pass

    markets = r.json()['data']


    if request.method == 'POST':
        # get the form info
        market = request.POST['market_name']
        condition = request.POST['condition']
        price = int(request.POST['price'])
        quantity = 1

        user_id = str(request.user.pk)


        # Check that a market exists
        if market not in [market['marketName'] for market in markets]:
            # Market doesn't exist
            print('market not found')
            return None

        # Map market names to IDS
        markets = {market['marketName']: market['marketId'] for market in r.json()['data']}

        # Get market ID
        market_id = markets[market]

        # print('MARKET ID', market_id)

        # Get asset for correct condition
        # Make a BUY request for every condition <= condition

        while True:
            try:
                r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/get_assets/%s/' % (market_id,), params={
                    "queries": ['"assetName" = \'' + condition + '\'']
                }, headers = headers)
                break
            except:
                pass

        # print(r.json())
        asset_id = r.json()['data'][0]

        # print('ASSET_ID:', asset_id)

        # Post new listing
        params = {
            'assetId': asset_id,
        }

        body = json.dumps({
            'price': price,
            'qty': quantity,
            'userId': user_id,
        })

        while True:
            try:
                r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/bids/%s/' % (market_id,), params = params, data=body, headers = headers)
                break
            except:
                pass

        # print(r.json())
        # Make an Order object linked to the user
        '''
        if r.json()['message'] != 'Order filled!':
            order_id = r.json()['data']['order']['_id']
        else:'''
        order_id = r.json()['data']['order']['orderId']

        order = Order(trader_name=request.user.profile, market_name=market, order_id=order_id)
        order.save()

        check_order_filled(request)

        return HttpResponseRedirect(reverse('index'))


    else:
        context = dict()
        context['markets'] = markets
        return render(request, 'main/buy.html', context)


def get_order_book(request):
    if True or request.method == 'POST':
        side = 'bids'
        try:
            r = requests.get(
                'http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/' + side + '/',
                params={}, headers=headers)
            print(r)
            info = r.json()['data']
            print(info)
            print(len(info))
            print(len(info[0]))
        except Exception as e:
            print("Request to API failed: " + e)

        return render(request, 'main/view_market.html')
    else:
        return render(request, 'main/view_market.html')


def check_order_filled(request):
    try:
        order_set = Order.objects.all()
        print(order_set)
        threshold_time = time.time() * 1000 - 120000

        while True:
            try:
                r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/transactions/',
                                 params={"timestampLower": str(threshold_time)}, headers=headers, timeout=0.1)
                break
            except:
                pass

        print("trades: ", r, r.json())
        info = r.json()['data']

        for trade in info:
            print(trade)
            print(trade['timestamp'], threshold_time)
            if trade['timestamp'] > threshold_time:
                for order in order_set:
                    print(order.order_id, order.notified)
                    if str(order.order_id) in (trade['askOrderId'], trade['bidOrderId']) and order.notified == "N":
                        print("Order was filled and belongs to user. Send notification")
                        order.notified = "Y"
                        order.save()
                        trade_price = trade['askPrice'] if trade['askTimestamp'] < trade['bidTimestamp'] else trade[
                            'bidPrice']
                        order_side = "sell" if str(order.order_id) == trade['askOrderId'] else "buy"
                        send_notification(order, trade_price, order_side)

    except Exception as e:
        print("Request to API failed: " + str(e))

    return False


def send_notification(order, trade_price, order_side):
    target_number = str(order.trader_name.phone_number)
    target_mail = str(order.trader_name.email)
    print("Phone Number?: ", order.trader_name.phone_number)

    account_sid = 'AC6dd084097904f1cf92ad8bc2b358fa87'
    auth_token = '113f188d5e893c3b3abaea5e6a0ccd40'
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body="Hi {}! Your {} order for a {} ({}) has been completed at ${}!   ".format(
                order.trader_name.user.username,
                order_side,
                order.market_name,
                order.order_id,
                trade_price)
                 + str(datetime.datetime.now()) + "   -DormMarket",
            from_='+16176185707',
            to='+1' + target_number
        )
        print("SMS sent: ", message.sid)
    except Exception as e:
        print("Invalid phone number or something: " + str(e))

    try:
        mail.send_mail(target_mail, "Your DormMarket order was successfully processed!",
                       """
Dear {},
    Congratulations! Your {} order for a {} ({}) has been completed at ${}!
    View the details at DormMarket.com/orders.

Regards,
    DormMarket Team
                       """.format(order.trader_name.user.username,
                                  order_side, order.market_name, order.order_id, trade_price)
                       )
    except Exception as e:
        print("Invalid email or something:" + str(e))



def buy_now(request, market_name, condition):
    user_id = str(request.user.pk)
    quantity = 1

    # Get market ID
    while True:
        try:
            r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/markets/', params={}, headers = headers, timeout=0.1)
            # Map market names to IDS
            markets = {market['marketName']: market['marketId'] for market in r.json()['data']}

            # Get market ID
            market_id = markets[market_name]

            break
        except:
            pass


    # Get asset for correct condition
    while True:
        try:
            r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/assets/get_assets/%s/' % (market_id,), params={
                "queries": ['"assetName" = \'' + condition + '\'']
            }, headers = headers, timeout = 0.1)
            break
        except:
            pass

    print('ASSETS:', r.json())

    asset_id = r.json()['data'][0]


    # Get best price
    while True:
        try:
            # get lowest asking price
            r = requests.get('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/asks/lowest_ask', params={'assetId': asset_id}, headers = headers, timeout = 0.1)
            print(r.json())
            price = int(r.json()['data'][0]['price'])
            break
        except:
            pass

    # Post new listing
    params = {
        'assetId': asset_id,
    }

    body = json.dumps({
        'price': price,
        'qty': quantity,
        'userId': user_id,
    })

    while True:
        try:
            r = requests.post('http://nasdaqhackathon-258550565.us-east-1.elb.amazonaws.com:8080/api/orders/bids/%s/' % (market_id,), params = params, data=body, headers = headers, timeout = 0.1)
            break
        except:
            pass

    print(r.json())

    # Make an Order object linked to the user
    if r.json()['message'] != 'Order filled!':
        order_id = r.json()['data']['order']['_id']
    else:
        order_id = r.json()['data']['order']['orderId']

    order = Order(trader_name=request.user.profile, market_name=market_name, order_id=order_id)
    order.save()
    print('order saved!')

    check_order_filled(request)

    return HttpResponseRedirect(reverse('index'))
