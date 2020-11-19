from django.contrib import admin
from django.urls import path, include
from django.views import generic

from blog.views import (
    index, product_detail, products, orders, add_product, Login, AddProductView,
    ProductListView, ProductDetailView, AddProductFormView, AddProductCreateView,
    UpdateProductView, UserDetailView, UserProfileView
)

from blog.api.views import ProductViewSet, LoginView
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'api-products', ProductViewSet, basename='product')

urlpatterns = [
    # path('login', login),
    path('base', generic.TemplateView.as_view(template_name='base.html')),
    path('login', Login.as_view()),
    path('index/<int:person_id>', index),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('products', ProductListView.as_view()),
    # path('add_product', add_product),
    # path('add_product', AddProductView.as_view()),
    # path('add_product', AddProductFormView.as_view()),
    path('add_product', AddProductCreateView.as_view()),
    path('update_product/<int:pk>', UpdateProductView.as_view()),
    path('add_product_duplicate', generic.RedirectView.as_view(url='/login')),
    path('orders/<int:user_id>', orders),
    path('user/<int:pk>', UserDetailView.as_view()),
    path('user-profile', UserProfileView.as_view()),


    # APIS
    path('api-login', LoginView.as_view())
] + router.urls

