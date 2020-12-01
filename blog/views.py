import datetime
from django.contrib.auth import login, logout
from django.contrib.auth import models as django_models
from django.views import generic, View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

# Create your views here.
from blog.models import Product, Order, ProductLike
from blog.forms import ProductForm, LoginForm, PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def index(request, person_id):
	person = User.objects.filter(id=person_id).first()
	return HttpResponse('hello we are live now.' + person.name if person else 'nothing')


class LikeProduct(LoginRequiredMixin, View):
	
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)
		
	def post(self, request, *args, **kwargs):
		product_id = kwargs.get('pk')
		product = get_object_or_404(Product, id=product_id)
		ProductLike.objects.get_or_create(
			product=product, user=self.request.user
		)
		return HttpResponse('success')


class PasswordResetView(LoginRequiredMixin, generic.FormView):
	form_class = PasswordResetForm
	success_url = '/products'
	template_name = 'password_reset.html'
	login_url = '/login'

	def form_valid(self, form):
		"""If the form is valid, redirect to the supplied URL."""
		self.request.user.set_password(form.cleaned_data['new_password'])
		self.request.user.save()
		update_session_auth_hash(self.request, self.request.user)
		return super().form_valid(form)
		
	def post(self, request, *args, **kwargs):
		form = self.get_form()
		form.user =  self.request.user
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)


class ManagerRequiredMixin(AccessMixin):
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated or not hasattr(self.request.user, 'userprofile') or not self.request.user.userprofile.is_manager:
			return self.handle_no_permission()
		return super().dispatch(request, *args, **kwargs)


class DeleteProductView(ManagerRequiredMixin, generic.DeleteView):
	"""
	Only manager can delete the product
	"""
	# model = Product
	# fields = ['name', 'price', 'image']
	success_url = '/products'
	# template_name = 'add_product.html'
	# form_class = ProductForm
	model = Product
	login_url = '/login'
	
	def get(self, request, *args, **kwargs):
		return self.delete(request, *args, **kwargs)

class UpdateProductView(LoginRequiredMixin, generic.UpdateView):
	# model = Product
	# fields = ['name', 'price', 'image']
	success_url = '/products'
	template_name = 'add_product.html'
	form_class = ProductForm
	model = Product
	login_url = '/login'
	
	def get_queryset(self):
		if hasattr(self.request.user, 'userprofile') and self.request.user.userprofile.is_manager:
			return super().get_queryset()
		return super().get_queryset().filter(created_by=self.request.user)
	

class AddProductCreateView(LoginRequiredMixin, generic.CreateView):
	login_url = '/login'
	# model = Product
	# fields = ['name', 'price', 'image']
	success_url = '/products'
	template_name = 'add_product.html'
	form_class = ProductForm
	# def form_valid(self, form):
	# 	"""If the form is valid, save the associated model."""
	# 	print('212121')
	# 	self.object = form.save()
	# 	# print('212121')
	# 	if self.request.user.is_authenticated:
	# 		self.object.created_by = self.request.user
	# 		self.object.save()
	# 	return super().form_valid(form)
	# 
	def get_success_url(self):
		if self.request.user.is_authenticated:
			self.object.created_by = self.request.user
			self.object.save()
		return super().get_success_url()


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


def login_function_base_view(request):
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
					return redirect('/user-profile')
				else:
					return render(request, 'login.html', {'form': form, 'error': 'Invalid Creds'})
			else:
				return render(request, 'login.html', {'form': form, 'error': 'User not found'})
		else:
			return render(request, 'login.html', {'form': form})


def product_detail(request, product_id):
	product = Product.objects.filter(id=product_id).first()
	return render(request, 'product_detail.html', {'product': product})


class UserProfileView(LoginRequiredMixin, generic.DetailView):
	login_url = '/login'
	model = User
	template_name = 'user_detail.html'
	context_object_name = 'user'

	def get_object(self):
		return self.request.user
			
	# def get(self, request):
	# 	if not self.request.user.is_authenticated:
	# 		return redirect('/login')
	# 	return super().get(self, request)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['products'] = Product.objects.filter(created_by=self.get_object())
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
	paginate_by = 25
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


# Functionalities
# Django functionality.
# 1. Add new blog (with and without logged in user)
# 2. if user is logged-in, it will  not show user dropdown during blog add and current logged in user should be linked with created_by
# 3. update blog and delete blog functionality.
# 4. user will be able to update only own add blog, so that no one can update blog added by someone else.
# 5. Delete blog functionality
# 6. Signup feature
# 7. Login and logout feature.
# 8. Blog list functionality.
# 9. show all the details of blog on detail page like title, description, date, image and added by
# 10. show user profile page and show all blog added by that user on that page.
# 11. update profile page.
# 12. show count in user profile of total number of blog created by that user. (hint-> use count query)

# DRF functionalty:
# 1. Login and signup
# 2. logout
# 3. Blog list, detail, update and delete api
# 4. user profile api which will have all blog created by that user.
# 5. user can update only self created blog.
# 6. show count in user profile of total number of blog created by that user.
# 7. create some api using viewset and view both.
# 8. in blog serilizer, send detail of created_by user using nested serializer.
# 10. first_name and last_name should be required in signup API.





