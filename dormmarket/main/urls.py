from django.conf.urls import url
from django.urls import include, path
from . import views
from django.urls import path, include

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^debug/$', views.debug, name='debug'),
    url(r'^orders/$', views.trade_list, name='orders'),
    path('sell', views.sell, name="sell")
]
