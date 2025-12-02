from django.urls import path
from . import views

urlpatterns = [
	path('products/', views.list_products, name='amzon-product-list'),
	path('products/<int:pk>/', views.product_detail, name='amzon-product-detail'),
	# Template / web views
	path('web/products/', views.product_list_web, name='amzon-product-list-web'),
	path('web/products/create/', views.product_create_web, name='amzon-product-create-web'),
	path('web/products/<int:pk>/edit/', views.product_edit_web, name='amzon-product-edit-web'),
	path('web/products/<int:pk>/delete/', views.product_delete_web, name='amzon-product-delete-web'),
]

