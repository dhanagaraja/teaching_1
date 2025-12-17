from django.urls import path, include
from rest_framework.routers import SimpleRouter
from amzon.views import ProductViewSet, CityViewSet, api_index, api_products, api_cities

# Create a router and register the ViewSets
router = SimpleRouter()
router.register(r'api/products', ProductViewSet, basename='product')
router.register(r'api/cities', CityViewSet, basename='city')

urlpatterns = [
    # Template Views
    path('', api_index, name='amzon_index'),
    path('products/', api_products, name='amzon_products'),
    path('cities/', api_cities, name='amzon_cities'),
    
    # API Endpoints
    path('', include(router.urls)),
]

