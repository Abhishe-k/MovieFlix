from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, SignInForm


# Create your views here.
from django.contrib.auth.models import User


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
            user = User.objects.create_user(username=username,
                            email=email,
                            first_name=first_name,
                            last_name=last_name, password=password)
            user.save()
            return redirect('loginUser')
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def loginUser(request):
    print(request.POST)
    if request.method == 'POST':
        form = SignInForm(request.POST)
        print(form.errors)
        if form.is_valid():
            # print(request.POST)
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                # return HttpResponse("LoggedIn: " + str(user))
                request.session['username'] = username
                return redirect('/home')
            else:
                return HttpResponse("Please enter valid credentials.")
    else:
        form = SignInForm()

    context = {
        'form': form,
    }
    return render(request, 'signin.html', context)


def home(request):
    if 'username' in request.session.keys():
        context = {
            'username': request.session['username']
        }
        return render(request, 'home.html', context)

    return HttpResponse("Not Logged In")


def logout(request):
    del request.session['username']
    return redirect('/home')

