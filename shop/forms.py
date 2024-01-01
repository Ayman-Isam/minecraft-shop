from django import forms
from django.db import models

class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())

class RedeemForm(forms.Form):
    code = forms.CharField(max_length=20)
