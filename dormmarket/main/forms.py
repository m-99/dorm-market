from django import forms


class SellForm(forms.Form):
	market = forms.CharField(label="Item category", max_length=100)
	condition = forms.ChoiceField(label="Condition", choices=[('poor', 'poor'), ('okay', 'okay'), ('good', 'good'), ('new', 'new')])
	description = forms.CharField(label="Description", max_length=256)
	price = forms.IntegerField()

class BuyForm(forms.Form):
	market = forms.CharField(label="Item category", max_length=100)
	condition = forms.ChoiceField(label="Condition", choices=[('poor', 'poor'), ('okay', 'okay'), ('good', 'good'), ('new', 'new')])
	description = forms.CharField(label="Description", max_length=256)
	price = forms.IntegerField()