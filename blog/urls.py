from django.contrib import admin
from django.urls import path, include
from django.views import generic

from blog.views import (
    index, product_detail, products, orders, add_product, Login, AddProductView,
    ProductListView, ProductDetailView
)

urlpatterns = [
    # path('login', login),
    path('base', generic.TemplateView.as_view(template_name='base.html')),
    path('login', Login.as_view()),
    path('index/<int:person_id>', index),
    path('product/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    path('products', ProductListView.as_view()),
    # path('add_product', add_product),
    path('add_product', AddProductView.as_view()),
    path('add_product_duplicate', generic.RedirectView.as_view(url='/login')),
    path('orders/<int:user_id>', orders),

]
