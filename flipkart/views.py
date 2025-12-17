import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from .models import Product, City
from .forms import ProductForm, CityForm

@csrf_exempt
def list_products(request):
	"""Return a list of products or create a new product when POSTed.

	Supports search (q) filtering on name/description and price range via
	min_price and max_price GET parameters.
	"""
	if request.method == 'GET':
		qs = Product.objects.all()
		# Search by name and description
		q = request.GET.get('q')
		if q:
			qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
		# Price range
		min_price = request.GET.get('min_price')
		max_price = request.GET.get('max_price')
		try:
			if min_price:
				qs = qs.filter(price__gte=Decimal(min_price))
			if max_price:
				qs = qs.filter(price__lte=Decimal(max_price))
		except InvalidOperation:
			# ignore invalid price filters
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
	else:
		return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def product_detail(request, pk):
	"""Retrieve, update or delete a product by pk."""
	product = get_object_or_404(Product, pk=pk)
	if request.method == 'GET':
		return JsonResponse({'product': {
			'id': product.pk,
			'name': product.name,
			'price': str(product.price),
			'description': product.description,
		}}, status=200)
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
	else:
		return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def list_cities(request):
	if request.method == 'GET':
		cities = list(City.objects.values())
		return JsonResponse({'cities': cities}, status=200)
	elif request.method == 'POST':
		try:
			data = json.loads(request.body)
			city = City.create_city(city=data.get('name'), state=data.get('state', ''))
			return JsonResponse({'id': city.pk, 'message': 'City created'}, status=201)
		except Exception as e:
			return JsonResponse({'error': str(e)}, status=400)
	else:
		return JsonResponse({'error': 'Method not allowed'}, status=405)


# Template-based CRUD views
def product_list_web(request):
	qs = Product.objects.all().exclude(active=False)
	q = request.GET.get('q')
	min_price = request.GET.get('min_price')
	max_price = request.GET.get('max_price')
	if q:
		qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

	try:
		if min_price:
			qs = qs.filter(price__gte=Decimal(min_price))
		if max_price:
			qs = qs.filter(price__lte=Decimal(max_price))
	except InvalidOperation:
		pass
	# products = [{'id':each.id, 'name':each.name, 'price':str(each.price), 'description':each.description} for each in qs]
	# import json
 
	# return JsonResponse(json.loads(json.dumps(products)), safe=False)

	context = {
		'products': qs,
		'q': q or '',
		'min_price': min_price or '',
		'max_price': max_price or '',
	}
	return render(request, 'flipkart/product_list.html', context)


def product_create_web(request):
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('flipkart-product-list-web')
	else:
		form = ProductForm()
	return render(request, 'flipkart/product_form.html', {'form': form, 'action': 'Create'})


def product_edit_web(request, pk):
	product = Product.objects.get(id=pk)
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES, instance=product)
		if form.is_valid():
			form.save()
			return redirect('flipkart-product-list-web')
	else:
		form = ProductForm(instance=product)
	return render(request, 'flipkart/product_form.html', {'form': form, 'action': 'Edit'})


def product_delete_web(request, pk):
	product = Product.objects.get(id=pk)
	if request.method == 'POST':
		product.active = False
		product.save()
		return redirect('flipkart-product-list-web')
	return render(request, 'flipkart/product_confirm_delete.html', {'product': product})


def city_list_web(request):
	cities = City.objects.all()
	return render(request, 'flipkart/city_list.html', {'cities': cities})


def city_create_web(request):
	if request.method == 'POST':
		form = CityForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('flipkart-city-list-web')
	else:
		form = CityForm()
	return render(request, 'flipkart/city_form.html', {'form': form, 'action': 'Create'})


def city_edit_web(request, pk):
	city = get_object_or_404(City, pk=pk)
	if request.method == 'POST':
		form = CityForm(request.POST, instance=city)
		if form.is_valid():
			form.save()
			return redirect('flipkart-city-list-web')
	else:
		form = CityForm(instance=city)
	return render(request, 'flipkart/city_form.html', {'form': form, 'action': 'Edit'})


def city_delete_web(request, pk):
	city = get_object_or_404(City, pk=pk)
	if request.method == 'POST':
		city.delete()
		return redirect('flipkart-city-list-web')
	return render(request, 'flipkart/city_confirm_delete.html', {'city': city})


@csrf_exempt
def city_detail(request, pk):
	city = get_object_or_404(City, pk=pk)
	if request.method == 'GET':
		return JsonResponse({'city': {
			'id': city.pk,
			'name': city.city,
			'state': city.state,
		}}, status=200)
	elif request.method in ('PUT', 'PATCH'):
		try:
			data = json.loads(request.body)
			city.update_city(**data)
			return JsonResponse({'message': 'City updated'}, status=200)
		except Exception as e:
			return JsonResponse({'error': str(e)}, status=400)
	elif request.method == 'DELETE':
		pk_deleted = city.delete_city()
		return JsonResponse({'message': 'City deleted', 'id': pk_deleted}, status=200)
	else:
		return JsonResponse({'error': 'Method not allowed'}, status=405)