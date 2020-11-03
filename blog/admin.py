from django.contrib import admin

# Register your models here.
from blog.models import User, Order, Product

admin.site.register(User)
admin.site.register(Order)
admin.site.register(Product)