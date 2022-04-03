from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from movie.forms import OrderForm, ImageForm, CommentForm
from .forms import SignUpForm, SignInForm
from movie.models import movie, actor, order, topmovie, profile, Comment
from django.core import serializers
# Create your views here.
from django.contrib.auth.models import User
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import imdb

movie_list_global = movie.objects.all().order_by("-year")
actor_list_global = actor.objects.all()


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

    topTen = topmovie.objects.filter()[:11]
    topTwenty = topmovie.objects.filter()[12:32]
    context = {
        'topTen': topTen,
        'topTwenty':topTwenty
    }
    if 'username' in request.session.keys():
        context['username'] = request.session['username']

        return render(request, 'home.html', context)
    return render(request, 'home.html',context)


def logout(request):
    del request.session['username']
    return redirect('/home')


def movies(request):
    global movie_list_global
    if not movie_list_global:
        print("fetching movies...")
        movie_list_global = movie.objects.all().order_by("-year")
        allmovies = movie_list_global
    else:
        allmovies = movie_list_global

    g1 = set(movie.objects.values_list('genre1', flat=True))

    g2 = set(movie.objects.values_list('genre2', flat=True))

    genre_list = list(set(g1 | g2))
    genre_list.remove('')
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

        print("List: ", allmovies)
        all_movies = allmovies.filter(query)
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
    context = {
            'movies': movies_list,
            'genres': genre_list,
            'years': year_list,
            'genre': genre,
            'year': year
        }

    if 'username' in request.session.keys():
        context['username'] = request.session['username']
        return render(request, 'movies.html', context)
    return render(request, 'movies.html', context)


def movieDetail(request, movie_id):
    global movie_list_global
    global actor_list_global

    if not movie_list_global:
        print("fetching movies...")
        movie_list_global = movie.objects.all().order_by("-year")
        actor_list_global = actor.objects.all()
        allmovies = movie_list_global
        allactors = actor_list_global
    else:
        allmovies = movie_list_global
        allactors = actor_list_global

    movie_by_id = allmovies.get(id=format(movie_id, '07'))
    print(movie_by_id)
    temp = None
    # for m in movie_by_id:
    temp = movie_by_id
    # items = Item.objects.filter(type_id=type_no)
    actors = allactors.filter(movieId=temp)
    temp2 = None
    for m in actors:
        temp2 = m

    ia = imdb.IMDb()

    comments = Comment.objects.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            new_comment.movie_Id = movie_by_id
            new_comment.username = request.session['username']

            new_comment.save()
    else:
        comment_form = CommentForm()

    actorList=[]
    if temp2.actor1 != '':
        actorList.append(ia.get_person(temp2.actor1)['name'])
    if temp2.actor2 != '':
        actorList.append(ia.get_person(temp2.actor2)['name'])
    if temp2.actor3 != '':
        actorList.append(ia.get_person(temp2.actor3)['name'])
    print(actorList)
    if 'username' in request.session.keys():
        context = {
            'username': request.session['username'],
            'movieData':temp,
            'actorList':actorList,
            'movie_detail': movie_by_id,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form
        }

        if request.POST:
            return redirect('/movie/' + str(movie_by_id.id))
        else:
            return render(request, 'movie.html', context)
    response = HttpResponse()
    return render(request, 'movie.html', {'movieData':temp,
                                          'movie_detail': movie_by_id,
                                          'comments': comments,
                                          })
    # para = '<p>' + str(type_by_id.id) + ': ' + str(type_by_id.name) + '</p>'
    # response.write(para)
    # return response


def profile_user(request):
    if 'username' not in request.session.keys():
        print('usad')
        return redirect('/signin')
    form = OrderForm()
    user = User.objects.get(username=request.session['username'])
    orderList = order.objects.all()
    # usr_img = profile.objects.get(username=request.session['username'])
    context = {'user': user, 'username': request.session['username'],'orderForm':form,'orderList':orderList}

    try:
        usr_img = profile.objects.get(username=request.session['username'])
        context['img'] = usr_img.image
    except:
        context['form'] = ImageForm()

    return render(request, 'profile.html', context)


def image_upload(request):
    if request.POST:
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            obj = profile(username=request.session['username'],
                          image=request.FILES['image'])
            obj.save()
            img_obj = request.FILES['image']
            print("HERE")
            return redirect('/profile')


def order_movie(request):
    if request.POST:
        obj = order(username=request.session['username'], title=request.POST['title'])
        obj.save()

        return redirect('/profile')