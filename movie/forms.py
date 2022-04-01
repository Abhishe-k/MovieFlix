from django import forms
from .models import profile


class ImageForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    username.disabled = True
    username.required = False

    class Meta:
        model = profile
        fields = ('username', 'image')


class OrderForm(forms.Form):
    title = forms.CharField(max_length=100)
