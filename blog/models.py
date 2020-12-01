from django.db import models
from django.contrib.auth import models as django_models
from django.contrib.auth.models import User


# class UserProfile(models.Model)
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	order_count = models.PositiveIntegerField(default=0)

# class User(models.Model):
# 	# id = models.IntegerField(primary_key=True)
# 	first_name = models.CharField(max_length=50)
# 	last_name = models.CharField(max_length=50)

# 	def __str__(self):
# 		return self.first_name + ' ' + self.last_name

# 	@property
# 	def full_name(self):
		# return self.first_name + ' ' + self.last_name

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_manager = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user) + '->' + str(self.is_manager)


class Category(models.Model):
	name = models.CharField(max_length=50)
	product_count = models.PositiveIntegerField()

	def __str__(self):
		return self.name + '->' + str(self.product_count)


class Product(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50)
	category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
	price = models.IntegerField()
	image = models.ImageField(blank=True, null=True)
	like_count = models.IntegerField(default=0)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name

class ProductLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)

	def __str__(self):
		return self.product.name + ' ' + self.user.first_name


class Order(models.Model):
	id = models.IntegerField(primary_key=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	order_time = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.user.name + '->' + self.product.name

# # Write query for printing product sorted via their price in ascending order
# #1. Filter part
# #2. Sorting part
# #3. Selecting part
# select field_1, field_2 from Table_name where filters order by order_field;
# update field_1=value_1, field_2=value_2 from Table_name where filters


# Product.objects.all().order_by('-price')


from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=Product, dispatch_uid="pre_save_product")
def pre_save_product(sender, instance, **kwargs):
	if not kwargs.get('created'):
		old_object = Product.objects.get(id=instance.id)
		print('pre-save start')
		print(old_object.name, old_object.price, 'this is old data')
		print(instance.name, instance.price, 'this is new data')
		print('pre-save end')

@receiver(post_save, sender=Product, dispatch_uid="update_product_count")
def update_product_count(sender, instance, **kwargs):
	if not kwargs.get('created'):
		old_object = Product.objects.get(id=instance.id)
		print('post-save start')
		print(old_object.name, old_object.price, 'this is old data')
		print(instance.name, instance.price, 'this is new data')
		print('post-save end')
	if kwargs.get('created') and instance.category:
		instance.category.product_count += 1
		instance.category.save()


@receiver(post_save, sender=ProductLike, dispatch_uid="post_save_product_like")
def post_save_product_like(sender, instance, **kwargs):
	if kwargs.get('created'):
		instance.product.like_count += 1
		instance.product.save()

@receiver(post_delete, sender=ProductLike, dispatch_uid="post_delete_product_like")
def post_delete_product_like(sender, instance, **kwargs):
	instance.product.like_count -= 1
	instance.product.save()

@receiver(post_delete, sender=Product, dispatch_uid="decrement_product_count")
def decrement_product_count(sender, instance, **kwargs):
	print(instance, kwargs)
	if instance.category:
		instance.category.product_count -= 1
		instance.category.save()


## Signal flow
# pre_save
# actual processing
# post_save

# class BlogLike(models.Model):
# 	user
# 	blog
# BlogLike.objects.filter(blog=blog).count()

# like_count = integer_field