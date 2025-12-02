from django.urls import path
from . import views

urlpatterns = [
	path('products/', views.list_products, name='product-list'),
	path('products/<int:pk>/', views.product_detail, name='product-detail'),
	path('cities/', views.list_cities, name='city-list'),
	path('cities/<int:pk>/', views.city_detail, name='city-detail'),
	# Template / web views
	path('web/products/', views.product_list_web, name='flipkart-product-list-web'),
	path('web/products/create/', views.product_create_web, name='flipkart-product-create-web'),
	path('web/products/<int:pk>/edit/', views.product_edit_web, name='flipkart-product-edit-web'),
	path('web/products/<int:pk>/delete/', views.product_delete_web, name='flipkart-product-delete-web'),
	path('web/cities/', views.city_list_web, name='flipkart-city-list-web'),
	path('web/cities/create/', views.city_create_web, name='flipkart-city-create-web'),
	path('web/cities/<int:pk>/edit/', views.city_edit_web, name='flipkart-city-edit-web'),
	path('web/cities/<int:pk>/delete/', views.city_delete_web, name='flipkart-city-delete-web'),
]
