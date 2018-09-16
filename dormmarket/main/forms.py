from django import forms
from .models import Order
from django.forms import ModelForm

class SellForm(ModelForm):
	class Meta:
		model = Order
		fields = ('description', 'market_name', 'order_id', 'image')

class BuyForm(forms.Form):
	market = forms.CharField(label="Item category", max_length=100)
	condition = forms.ChoiceField(label="Condition", choices=[('poor', 'poor'), ('okay', 'okay'), ('good', 'good'), ('new', 'new')])
	description = forms.CharField(label="Description", max_length=256)
	price = forms.IntegerField()