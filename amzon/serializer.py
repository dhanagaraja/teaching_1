"""
Serializers for flipkart models (Product and City).
"""
from rest_framework import serializers
from flipkart.models import Product, City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city', 'state', 'pin_code']


class ProductSerializer(serializers.ModelSerializer):
    location = CitySerializer(read_only=True)
    location_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    def validate(self, attrs):
        return attrs

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'description', 'active', 
            'image', 'location', 'location_id'
        ]
