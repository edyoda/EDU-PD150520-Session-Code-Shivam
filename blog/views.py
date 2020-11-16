import datetime
from django.contrib.auth import login, logout
from django.contrib.auth import models as django_models
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


class UpdateProductView(generic.UpdateView):
	# model = Product
	# fields = ['name', 'price', 'image']
	success_url = '/products'
	template_name = 'add_product.html'
	form_class = ProductForm
	model = Product


class AddProductCreateView(generic.CreateView):
	# model = Product
	# fields = ['name', 'price', 'image']
	success_url = '/products'
	template_name = 'add_product.html'
	form_class = ProductForm


class AddProductFormView(generic.FormView):
	form_class = ProductForm
	success_url = '/products'
	template_name = 'add_product.html'

	def form_valid(self, form):
		"""If the form is valid, redirect to the supplied URL."""
		form.save()
		return super().form_valid(form)


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
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = django_models.User.objects.filter(username=username).first()
			if user:
				if user.check_password(password):
					login(request, user)
					return redirect('/product/1')
				else:
					return render(request, 'login.html', {'form': form, 'error': 'Invalid Creds'})
			else:
				return render(request, 'login.html', {'form': form, 'error': 'User not found'})
		else:
			return render(request, 'login.html', {'form': form})


def product_detail(request, product_id):
	product = Product.objects.filter(id=product_id).first()
	return render(request, 'product_detail.html', {'product': product})


class UserProfileView(generic.DetailView):
	model = User
	template_name = 'user_detail.html'
	context_object_name = 'user'
	def get_object(self):
		if self.request.user.is_authenticated:
			return self.request.user
		else:
			return None
			
	def get(self, request):
		if not self.request.user.is_authenticated:
			return redirect('/login')
		return super().get(self, request)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# context['products'] = Product.objects.filter(created_by=self.get_object())
		return context


class UserDetailView(generic.DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user'
	
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(created_by=self.get_object())
        return context


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

from rest_framework.viewsets import ModelViewSet
from blog.serializers import ProductSerializer

class ProductViewSet(ModelViewSet):

	queryset = Product.objects.all()
	serializer_class = ProductSerializer
