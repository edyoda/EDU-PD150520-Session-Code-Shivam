from django.db import models
class User(models.Model):
	# id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Product(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=50)
	price = models.IntegerField()
	image = models.ImageField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

	def __str__(self):
		return self.name

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







