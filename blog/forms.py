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


class PasswordResetForm(forms.Form):
    current_password = forms.CharField(max_length=50)
    new_password = forms.CharField(max_length=50)
    confirm_password = forms.CharField(max_length=50)

    def clean(self):
        if not self.user.check_password(self.cleaned_data['current_password']):
            raise forms.ValidationError('Current password is not correct')

        if self.cleaned_data['new_password'] != self.cleaned_data['confirm_password']:
            raise forms.ValidationError('Password do not match')
        return self.cleaned_data

