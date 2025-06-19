from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    size = forms.CharField(required=False, widget=forms.Select(choices=[]))
    color = forms.CharField(required=False, widget=forms.Select(choices=[]))

    def __init__(self, *args, **kwargs):
        sizes = kwargs.pop('sizes', None)
        colors = kwargs.pop('colors', None)
        super().__init__(*args, **kwargs)

        if sizes:
            self.fields['size'].widget.choices = sizes
        if colors:
            self.fields['color'].widget.choices = colors
class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

