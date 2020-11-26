from django import forms

from blog.models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('id', 'created_by')


class LoginForm(forms.Form):

    username = forms.CharField(initial='', help_text='Enter username')
    password = forms.CharField(max_length=50)

    class Meta:
        fields = ('username', 'password')
