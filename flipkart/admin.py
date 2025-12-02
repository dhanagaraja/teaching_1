from django.contrib import admin
from .models import Product, City


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'price')


# @admin.register(City)
# class CityAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'name', 'state')

