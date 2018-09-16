from django.urls import include, path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('debug/', views.debug, name='debug'),
    path('orders/', views.trade_list, name='orders'),
    path('sell/', views.sell, name="sell"),
    path('buy/', views.buy, name="buy"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

