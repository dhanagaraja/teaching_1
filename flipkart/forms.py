from django import forms
from .models import Product, City


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'location', 'active']


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city', 'state', 'pin_code']
