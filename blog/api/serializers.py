from rest_framework import serializers
from blog.models import Product, Order
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'full_name')

    def get_full_name(self, instance):
        return instance.first_name  + ' ' + instance.last_name


class TokenSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Token
        fields = ('user', 'key')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ('username', 'password')

    def validate(self, data):
        user = User.objects.filter(username=data['username']).first()
        if not user:
            raise serializers.ValidationError('user not found')
        if not user.check_password(data['password']):
            raise serializers.ValidationError('Invalid credential')
        return data

    def login(self, data):
        user = User.objects.filter(username=data['username']).first()
        token, created = Token.objects.get_or_create(user=user)
        return TokenSerializer(token).data        


class SignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=25, write_only=True)
    confirm_password = serializers.CharField(max_length=25, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('Password does not match')
        return data

    def save(self, data):
        password = data.pop('password')
        data.pop('confirm_password')
        
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()
        return user


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
