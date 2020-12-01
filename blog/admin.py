from django.contrib import admin

# Register your models here.
from blog.models import Order, Product, Category, UserProfile, ProductLike

# admin.site.register(User)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(ProductLike)