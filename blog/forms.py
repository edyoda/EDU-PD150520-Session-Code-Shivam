from django import forms

from blog.models import Product

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ('id',)


class LoginForm(forms.Form):

    username = forms.CharField(initial='admin', help_text='Enter username or email')
    password = forms.CharField(max_length=50, widget=forms.Textarea(attrs={'class': 'message-input'}))


    class Meta:
        fields = ('username', 'password')

    def clean_username(self):
        data = self.cleaned_data["username"]
        if len(data) < 3:
            raise forms.ValidationError('Username must be atleast 3 char long')
        
        return data
    

    def clean(self):
        self.cleaned_data["username"]
        raise forms.ValidationError('Username and Password is not correct')
