from django import forms
from .models import profile, Comment


class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))
    class Meta:
        model = profile
        fields = ('image',)


class OrderForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title")


class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':5, 'cols': 100}))

    class Meta:
        model = Comment
        fields = ('body',)

