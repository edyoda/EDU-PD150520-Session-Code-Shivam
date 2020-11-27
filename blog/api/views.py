from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics, mixins, views
from blog.api.serializers import (
	ProductSerializer, ProductSerializerWithId, LoginSerializer, SignUpSerializer,
	UserSerializer
)
from rest_framework.permissions import IsAuthenticated
from blog.models import Product


class ProductViewSet(ModelViewSet):

	queryset = Product.objects.all()
	pagination_class = PageNumberPagination

	# serializer_class = ProductSerializer

	def get_serializer_class(self):
		print(self.action)
		if self.action == 'create':
			return ProductSerializer
		return ProductSerializerWithId


class UserProfileApiView(generics.RetrieveAPIView):
	serializer_class = UserSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		print(self.request.user)
		return self.request.user


class LoginView(APIView):
	serializer_class = LoginSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		return Response(serializer.login(serializer.validated_data))


class SignUpView(APIView):
	serializer_class = SignUpSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save(serializer.validated_data)
		return Response(serializer.data)
