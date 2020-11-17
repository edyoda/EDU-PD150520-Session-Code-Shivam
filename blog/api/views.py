from rest_framework.viewsets import ModelViewSet
from blog.api.serializers import ProductSerializer
from blog.models import Product


class ProductViewSet(ModelViewSet):

	queryset = Product.objects.all()
	serializer_class = ProductSerializer
