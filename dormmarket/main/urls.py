from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
# import dormmarket.main.views as core_views

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# try:
#     from dormmarket.main import views
# except Exception as e:
#     print(e)

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
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'templates/signup.html', {'form': form})

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
]