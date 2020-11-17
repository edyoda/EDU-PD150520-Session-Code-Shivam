from rest_framework import serializers
from blog.models import Product, Order
from django.contrib.auth.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        fields = ('name', 'age')

    def validate_username(self, data):
        print(data, 'under validate_username')
        if len(data) < 3:
            raise serializers.ValidationError('Length should be at least 3.')
        return data

    def validate(self, data):
        print(data, 'under validate')
        user = User.objects.filter(username=data['username'])
        if not user:
            raise serializers.ValidationError('user not found')
        return data


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
