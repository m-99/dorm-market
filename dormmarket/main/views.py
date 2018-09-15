from django.http import HttpResponse
from django.shortcuts import render

# first thing that user sees -> browse
def index(request):
    return HttpResponse("hey bb ur at the main index")

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
