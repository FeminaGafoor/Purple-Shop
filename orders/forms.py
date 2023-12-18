from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user_name','email','phone','address_1','address_2','city','state','country','order_note']