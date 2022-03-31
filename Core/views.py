from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, SignInForm
from movie.models import movie
from django.core import serializers
# Create your views here.
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import imdb


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
    ia = imdb.IMDb()
    top = ia.get_top250_movies()
    topFive = top[:5]
    print(list(topFive))
    if 'username' in request.session.keys():
        context = {
            'username': request.session['username'],
            'top':top,
            'topFive':list(topFive)

        }
        return render(request, 'home.html', context)
    return render(request,'home.html')


def logout(request):
    del request.session['username']
    return redirect('/home')

def movies(request):

    allmovies = movie.objects.all()
    g1 = set(movie.objects.values_list('genre1', flat=True))

    g2 = set(movie.objects.values_list('genre2', flat=True))

    genre_list = list(set(g1|g2))
    genre_list.remove('')
    # min_year = movies.objects.all.min('year')
    year_list = range(1800, 2023)
    if "genre" in request.POST.keys():
        genre = request.POST["genre"]
    else:
        genre = "all"
    if "year" in request.POST.keys():
        year = request.POST["year"]
    else:
        year = ""

    paginator = Paginator(allmovies, 18)
    page = request.GET.get('page')
    print(page)
    try:
        movies_list = paginator.page(page)
    except PageNotAnInteger:
        movies_list = paginator.page(1)
    except EmptyPage:
        movies_list = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        searchmovie = request.POST["searchmovie"]
        print(searchmovie)
        year = request.POST["year"]
        genre = request.POST["genre"]
        query = Q(year__lt=2023)
        if genre != "all":
            query = Q(genre1=genre)
            query.add(Q(genre2=genre), Q.OR)
        if searchmovie:
            query.add(Q(title__contains=searchmovie), Q.AND)
        if year:
            query.add(Q(year=year), Q.AND)


        all_movies = movie.objects.filter(query)
        allmovies = all_movies
        print(allmovies)


        # allmovies = movie.objects.filter(title__contains=searchmovie, year=year)
        paginator = Paginator(allmovies, 18)
        page = request.GET.get('page')
        print(page)
        try:
            movies_list = paginator.page(page)
        except PageNotAnInteger:
            movies_list = paginator.page(1)
        except EmptyPage:
            movies_list = paginator.page(paginator.num_pages)
        print(movies_list)
    if 'username' in request.session.keys():
        context = {
            'username': request.session['username'],
            'movies': movies_list,
            'genres': genre_list,
            'years': year_list,
            'genre':genre,
            'year':year
        }
        return render(request, 'movies.html', context)
    return render(request,'movies.html',{'movies':list(allmovies)})
def movieDetail(request, movie_id):
        movie_by_id=  movie.objects.filter(id=format(movie_id,'07'))
        print(movie_by_id)
        temp = None
        for m in movie_by_id:
            temp = m
        # items = Item.objects.filter(type_id=type_no)
        if 'username' in request.session.keys():
            context = {
                'username': request.session['username'],
                'movieData':temp
            }
            return render(request, 'movie.html', context)
        response = HttpResponse()
        return render(request, 'movie.html', {'movieData':temp})
        # para = '<p>' + str(type_by_id.id) + ': ' + str(type_by_id.name) + '</p>'
        # response.write(para)
        # return response