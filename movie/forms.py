from django import forms
from .models import profile


class ImageForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ('image',)


class OrderForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title")

