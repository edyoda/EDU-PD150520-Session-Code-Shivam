from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet
from blog.api.serializers import ProductSerializer, ProductSerializerWithId, LoginSerializer
from blog.models import Product


class ProductViewSet(ModelViewSet):

	queryset = Product.objects.all()
	# serializer_class = ProductSerializer

	def get_serializer_class(self):
		print(self.action)
		if self.action == 'create':
			return ProductSerializer
		return ProductSerializerWithId


class LoginView(APIView):
	serializer_class = LoginSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response(serializer.login(serializer.validated_data))
