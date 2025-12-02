import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from .models import Product
from .forms import ProductForm

@csrf_exempt
def list_products(request):
	if request.method == 'GET':
		qs = Product.objects.all()
		q = request.GET.get('q')
		if q:
			qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
		min_price = request.GET.get('min_price')
		max_price = request.GET.get('max_price')
		try:
			if min_price:
				qs = qs.filter(price__gte=Decimal(min_price))
			if max_price:
				qs = qs.filter(price__lte=Decimal(max_price))
		except InvalidOperation:
			pass
		products = list(qs.values())
		return JsonResponse({'products': products}, status=200)
	elif request.method == 'POST':
		try:
			data = json.loads(request.body)
			product = Product.create_product(name=data.get('name'), price=data.get('price', 0), description=data.get('description', ''))
			return JsonResponse({'id': product.pk, 'message': 'Product created'}, status=201)
		except Exception as e:
			return JsonResponse({'error': str(e)}, status=400)
	return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def product_detail(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if request.method == 'GET':
		return JsonResponse({'product': {'id': product.pk, 'name': product.name, 'price': str(product.price), 'description': product.description}}, status=200)
	elif request.method in ('PUT', 'PATCH'):
		try:
			data = json.loads(request.body)
			product.update_product(**data)
			return JsonResponse({'message': 'Product updated'}, status=200)
		except Exception as e:
			return JsonResponse({'error': str(e)}, status=400)
	elif request.method == 'DELETE':
		pk_deleted = product.delete_product()
		return JsonResponse({'message': 'Product deleted', 'id': pk_deleted}, status=200)
	return JsonResponse({'error': 'Method not allowed'}, status=405)


# Template-based CRUD views for amzon
def product_list_web(request):
	qs = Product.objects.all()
	q = request.GET.get('q')
	if q:
		qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')
	try:
		if min_price:
			qs = qs.filter(price__gte=Decimal(min_price))
		if max_price:
			qs = qs.filter(price__lte=Decimal(max_price))
	except InvalidOperation:
		pass
	products = qs
	context = {'products': products, 'q': q or '', 'min_price': min_price or '', 'max_price': max_price or ''}
	return render(request, 'amzon/product_list.html', context)


def product_create_web(request):
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('amzon-product-list-web')
	else:
		form = ProductForm()
	return render(request, 'amzon/product_form.html', {'form': form, 'action': 'Create'})


def product_edit_web(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if request.method == 'POST':
		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
			return redirect('amzon-product-list-web')
	else:
		form = ProductForm(instance=product)
	return render(request, 'amzon/product_form.html', {'form': form, 'action': 'Edit'})


def product_delete_web(request, pk):
	product = get_object_or_404(Product, pk=pk)
	if request.method == 'POST':
		product.delete()
		return redirect('amzon-product-list-web')
	return render(request, 'amzon/product_confirm_delete.html', {'product': product})

