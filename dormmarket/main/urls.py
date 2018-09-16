from django.urls import include, path, re_path
from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('debug/', views.debug, name='debug'),
    path('orders/', views.trade_list, name='orders'),
    path('sell/', views.sell, name="sell"),
    path('buy/', views.buy, name="buy"),
]
