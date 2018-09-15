from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("hey bb ur at the main index")
