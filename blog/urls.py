from django.contrib import admin
from django.urls import path, include
from blog.views import index, product_detail, products, orders, add_product, login

urlpatterns = [
    path('login', login),
    path('index/<int:person_id>', index),
    path('product/<int:product_id>', product_detail, name='product_detail'),
    path('products', products),
    path('add_product', add_product),
    path('orders/<int:user_id>', orders)
]
