from main.models import Profile, Order
from django.contrib.auth.models import User
from datetime import datetime

# now = datetime.now()
# newuser = User(is_superuser=True, last_login=now, username="test 3", password="test 3")
# newuser.save()
# p = Profile(user = newuser)
# p.save()
order = Order(item_name="Macbook Pro", market_name="macbook")
# order = Order(item_name="Microwave Fancy", market_name="Microwave")
order.save()