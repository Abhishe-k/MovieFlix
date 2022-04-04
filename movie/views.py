from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .data import Data
from .forms import ImageForm, OrderForm, CommentForm
from .models import profile, order, movie, userlikes
from django.contrib.auth.models import User


def movies(request):
    d = Data()
    d.get_movies(False)

    return HttpResponse('Movies are saved to database.')


def top_250(request):
    d = Data()
    top250 = d.get_movies(True)

    print(len(top250))

    return render(request, 'home.html', {'top250': top250})


def update_image(request):
    d = Data()
    d.update_image()

    return HttpResponse('All images are updated.')


def image_upload(request):
    if request.POST:
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid():
            obj = profile(username=request.session['username'],
                          image=request.FILES['image'])
            obj.save()
            img_obj = request.FILES['image']
            print("HERE")
            return render(request, 'image.html', {'img_obj': img_obj})
    else:
        form = ImageForm()

    return render(request, 'image.html', {'form': form})


def view_image(request):
    if 'username' in request.session.keys():
        image = profile.objects.get(username=request.session['username'])
        return render(request, 'displayimage.html', {'img_obj': image.image,
                                                     'media_url': settings.MEDIA_URL})


def comment_details(request):
    movie_detail = get_object_or_404(movie, slug=slug)
    comments = movie_detail.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            new_comment.movie_detail = movie_detail
            new_comment.username = request.session['username']

            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'comment.html', {'movie_detail': movie_detail,
                                            'comments': comments,
                                            'new_comment': new_comment,
                                            'comment_form': comment_form})


def likes(request, m_id):
    # try:
    user = User.objects.get(username=request.session['username'])
    print(user.email)
    movie_title = movie.objects.get(id=format(m_id, '07'))
    print(movie_title)
    userlike = userlikes.objects.filter(username=request.session['username'], movie_id=m_id)
    if not userlike:
        obj = userlikes(movie_id=movie_title, movie=movie_title.title, username=user.username, likes=True)
        obj.save()
        return HttpResponse("Liked")
    return HttpResponse("Already Liked")

