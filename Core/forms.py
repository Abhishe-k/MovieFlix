from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True)
    email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True)
    first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=True)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Confirm your password.')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def _init_(self, *args, **kwargs):
        super(SignUpForm, self)._init_(*args, **kwargs)

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Password do not match, try again!'])

        return self.cleaned_data


class SignInForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def _init_(self, *args, **kwargs):
        super(SignInForm, self)._init_(*args, **kwargs)

    def clean(self):
        super(SignInForm, self).clean()
        password = self.cleaned_data.get('password')

        return self.cleaned_data