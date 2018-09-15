import os, sys
sys.path.append('./')
os.environ['DJANGO_SETTINGS_MODULE']='dormmarket.settings'
from main.models import Profile, Order

prof = Profile()
o = Order(item_name="Mac", price=2000)
o.save()