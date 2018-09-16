from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Order


class SellForm(ModelForm):
    class Meta:
        model = Order
        fields = ('description', 'market_name', 'order_id', 'image')


class BuyForm(forms.Form):
    market = forms.CharField(label="Item category", max_length=100)
    condition = forms.ChoiceField(label="Condition",
                                  choices=[('poor', 'poor'), ('okay', 'okay'), ('good', 'good'), ('new', 'new')])
    description = forms.CharField(label="Description", max_length=256)
    price = forms.IntegerField()


class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'password1', 'password2',)
