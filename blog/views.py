import datetime
from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
# Create your views here.
from blog.models import User, Product, Order
from blog.forms import ProductForm, LoginForm

def index(request, person_id):
	person = User.objects.filter(id=person_id).first()
	return HttpResponse('hello we are live now.' + person.name if person else 'nothing')


class AddProductView(View):
	def get(self, request):
		form = ProductForm()
		return render(request, 'add_product.html', {'form': form})
	
	def post(self, request):
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/products')
		else:
			return render(request, 'add_product.html', {'form': form})


def add_product(request):
	if request.method == 'GET':
		form = ProductForm()
		return render(request, 'add_product.html', {'form': form})
	else:
		form = ProductForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/products')
		else:
			return render(request, 'add_product.html', {'form': form})


def login(request):
	if request.method == 'GET':
		form = LoginForm()
		return render(request, 'login.html', {'form': form})
	else:
		form = LoginForm(request.POST)
		if form.is_valid():
			return redirect('/products')
		else:
			return render(request, 'login.html', {'form': form})


class Login(View):
	def get(self, request):
		form = LoginForm()
		return render(request, 'login.html', {'form': form})
	
	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			return redirect('/products')
		else:
			return render(request, 'login.html', {'form': form})


def product_detail(request, product_id):
	product = Product.objects.filter(id=product_id).first()
	return render(request, 'product_detail.html', {'product': product})


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'my_product'
	
    # def get_object(self):
    #     obj = self.get_queryset().filter(id=1).first()
    #     print(obj)
    #     return obj


class ProductListView(generic.ListView):
	# model = Product
	template_name = 'products.html'
	context_object_name = 'products'
	queryset = Product.objects.filter()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['now'] = datetime.datetime.now()
		return context


def products(request):
	products =  Product.objects.all()
	return render(request, 'products.html', {'products': products})

def orders(request, user_id):
	orders = Order.objects.filter(user_id=user_id)
	return render(request, 'orders.html', {'orders': orders})
