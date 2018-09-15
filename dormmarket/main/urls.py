from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name=''),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^debug/$', views.debug, name='debug'),
    url(r'^orders/$', views.trade_list, name='orders'),
]