"""
Amzon app views: REST API using Django REST Framework ViewSets.
APIs work with flipkart models (Product and City).
Returns JSON responses for all endpoints.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from django.shortcuts import render

from flipkart.models import Product, City
from amzon.serializer import ProductSerializer, CitySerializer


# Template Views for UI
def api_index(request):
    """Dashboard with API documentation."""
    return render(request, 'amzon/api_index.html')


def api_products(request):
    """Products management UI."""
    return render(request, 'amzon/api_products.html')


def api_cities(request):
    """Cities management UI."""
    return render(request, 'amzon/api_cities.html')

class Student:
   def __init__(self):
      self.name = "John"
      self.age = 21
   
   def study(self):
      return f"{self.name} is studying."
   
class ProductViewSet(viewsets.ModelViewSet):
   serializer_class = ProductSerializer

   def get_queryset(self):
      queryset = Product.objects.all().exclude(active=False)
      search = self.request.query_params.get('search')
      min_price = self.request.query_params.get('min_price')
      max_price = self.request.query_params.get('max_price')
      if search:
         queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search))

      # Price range filter
      if min_price:
         queryset = queryset.filter(price__gte=Decimal(min_price))
      if max_price:
         queryset = queryset.filter(price__lte=Decimal(max_price))

      return queryset
   
   def list(self, request, *args, **kwargs):
      """Override list to handle Decimal conversion errors."""
      try:
         queryset = self.get_queryset()
         serializer = self.get_serializer(queryset, many=True)
         return Response(serializer.data)

      except InvalidOperation:
         return Response({'error': 'Invalid price filter'}, status=status.HTTP_400_BAD_REQUEST)

   def retrieve(self, request, *args, **kwargs):
      """Retrieve a single product by ID."""
      # query = self.get_object()
      # query = Product.objects.get(id=kwargs.get('pk'))
      query = Product.objects.filter(id=kwargs.get('pk')).first()
      print(query)
      if query:
         serializer = ProductSerializer(query)
         return Response(serializer.data)
      else:
         return Response({'error': 'Product sdfg dsfg not found'}, status=status.HTTP_404_NOT_FOUND)
   
   def create(self, request, *args, **kwargs):
      """Create a new product."""
      print(request.data)
      serializer = ProductSerializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      object = serializer.save()
      # return Response(serializer.data, status=status.HTTP_201_CREATED)
      # object = Product.objects.create(**request.data)
      # return Response(ProductSerializer(object).data, status=status.HTTP_201_CREATED)
      # object = Product.objects.create(
      #    name=request.data.get('name'),
      #    price=request.data.get('price'),
      #    description=request.data.get('description'),
      #    location=City.objects.get(id=request.data.get('location')) if request.data.get('location') else None,
      #    active=request.data.get('active', True)
      # )
      return Response(ProductSerializer(object).data, status=status.HTTP_201_CREATED)

   def update(self, request, *args, **kwargs):
      return super().update(request, *args, **kwargs)

class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
