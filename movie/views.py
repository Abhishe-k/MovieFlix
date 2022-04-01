from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .data import Data
from .forms import ImageForm, OrderForm
from .models import profile, order


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

            return render(request, 'image.html', {'img_obj': img_obj})
    else:
        form = ImageForm(initial={'username': request.session['username']})

    return render(request, 'image.html', {'form': form})


def view_image(request):
    if 'username' in request.session.keys():
        image = profile.objects.get(username=request.session['username'])
        return render(request, 'displayimage.html', {'img_obj': image.image,
                                                     'media_url': settings.MEDIA_URL})


def order_movie(request):
    if request.POST:
        obj = order(username=request.session['username'], title=request.POST['title'])
        obj.save()
        return render(request, 'base.html', {'msg': 'Order placed successfully for ' + request.POST['title']})

