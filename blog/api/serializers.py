from rest_framework import serializers
from blog.models import Product, Order
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'full_name')

    def get_full_name(self, instance):
        return {1:2}


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ('name', 'password')

    def validate_username(self, data):
        print(data, 'under validate_username')
        if len(data) < 3:
            raise serializers.ValidationError('Length should be at least 3.')
        return data

    def validate(self, data):
        print(data, 'under validate')
        user = User.objects.filter(username=data['username']).first()
        if not user:
            raise serializers.ValidationError('user not found')
        if not user.check_password(data['password']):
            raise serializers.ValidationError('Invalid credential')
        return data

    def login(self, data):
        user = User.objects.filter(username=data['username']).first()
        return UserSerializer(user).data        

class ProductSerializerWithId(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name', 'price', 'id')

class ProductSerializer(serializers.ModelSerializer):

    combination = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'price', 'combination')

    def get_combination(self, instance):
        return instance.name + ' ' + str(instance.price)


# Mapping of DRF term and current HTTP method
# CRUD operation
# C -> create
# R -> retrive
# U -> update
# D -> delete


# mixins.CreateModelMixin -> POST,
# mixins.RetrieveModelMixin -> get,
# mixins.UpdateModelMixin -> PUT/PATCH,
# mixins.DestroyModelMixin -> Delete,
# mixins.ListModelMixin -> GET,
