from django import forms


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