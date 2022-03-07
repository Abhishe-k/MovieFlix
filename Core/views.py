from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, SignInForm


# Create your views here.
from .models import UserProfile


def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('form validation portion')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            user = UserProfile(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
            user.save()
            return redirect('loginUser')
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)
def loginUser(request):

    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = UserProfile.objects.get(email=email,password=password)
            print(user)
            if user is not None:
                print(user)
                return redirect('home')
            else:
                print("not authenticated")
    else:
        form = SignInForm()

    context = {
        'form': form,
    }
    return render(request, 'signin.html', context)

