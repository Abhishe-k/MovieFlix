import random

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from movie.forms import OrderForm, ImageForm, CommentForm
from movie.models import movie, actor, order, topmovie, profile, usertoken, userlikes, Comment, MovieOrder
from .forms import SignUpForm, SignInForm, ResetPasswordForm, ForgotPasswordForm, ContactForm
from django.core import serializers
# Create your views here.
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import imdb

from movie.models import Contact
import stripe

movie_list_global = movie.objects.all().order_by("-year")
actor_list_global = actor.objects.all()


def registerUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            print('form validation portion')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            temp_user = User.objects.filter(email=email)
            if temp_user:
                return HttpResponse("User with " + email + "already exist." + "<a href='/signup'>" + "Sign Up" + "</a>")

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

def forgot_password(request):
    if request.POST:
        user_email = request.POST['email']

        try:
            user = User.objects.get(email=user_email)
        except:
            return HttpResponse('User with ' + user_email + ' does not exist. Please enter valid email.' + "<a href='/forgotpassword'>" + " Forgot password?" + "</a>")
        if user:
            try:
                user_token =  usertoken.objects.get(email=user.email)
                token = user_token.id
            except:
                user_token = usertoken(username=user.username, email=user.email)
                user_token.save()
                token = usertoken.objects.get(email=user_email).id

            subject = 'Reset Password'
            message = ' You have requested to reset your password ' + user.username + \
                      "Please click the below link to reset your password http://127.0.0.1:8000/resetpassword"

            email_from = settings.EMAIL_HOST_USER
            recipient_list = []
            recipient_list.append(user_email)
            htmlmessage = """
                        <html lang="en">
                <head>
                  <title>Bootstrap Example</title>
                  <meta charset="utf-8">
                  <meta name="viewport" content="width=device-width, initial-scale=1">
                  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
                  <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.slim.min.js"></script>
                  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
                  <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
                </head>
                <body>
                <div class="container">
    
                """ \
                          + " <center><h2>Request to reset password of <strong> " + str(
                user.username) + " </strong>!</h2></center> " \
                            """
                            <div class="card">
                                                                                                   <div class="card-body" style="text-align: center">
                                                                                                     <h4 class="card-title"></h4>
                                                                                                     <p class="card-text">Hi, to reset your password, please click the below link: <strong>
            <a href="http://127.0.0.1:8000/resetpassword/"""+str(token) + ""\
                                 """
                                 ">Reset Password</a> </strong>" 
                                               </p>
                                              </div>
                                            </div>
                                          </div>
                                          </body>
                                          </html>
                                                  """
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=htmlmessage)
            print(email_from + str(recipient_list) + message + user_email)
            return render(request,"password_reset_done.html")
        else:
            return HttpResponse("User with this email not found. Please try again")
    else:
        form = ForgotPasswordForm()
    return render(request,"forgotpassword.html",{"form":form})

def change_password(request,token):
    print(request.POST)
    valid = False

    user_token = usertoken.objects.filter(id=token)[0]
    if user_token:
        valid = True
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            print(form.errors)
            if form.is_valid():
                # print(request.POST)
                password = request.POST['password']
                confirm_password = request.POST['confirm_password']
                user = User.objects.get(username=user_token.username)
                if user:
                    if password == confirm_password:
                        user.set_password(password)
                        user.save()
                        user_token.delete()
                        return redirect('/signin')
                    else:
                        return HttpResponse("Please enter valid credentials.")

        else:
            form = ResetPasswordForm()

        context = {
            'form': form,
            'valid': valid
        }
        return render(request, 'resetpassword.html', context)
    else:
        context = {
            'valid': valid
        }
        return render(request, 'resetpassword.html', context)


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

    if "rating" in request.POST.keys():
        rating = request.POST['rating']
    else:
        rating = 'high'

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
        if rating != "high":
            all_movies = allmovies.filter(query).order_by('rating')
        else:
            all_movies = allmovies.filter(query).order_by('-rating')

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
            'year': year,
            'rating': rating,
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
    # items = Item.objects.filter(type_id=type_no)
    if temp.runtime != '':
        temp.runtime = temp.runtime.split("'")[1]
    print(temp.runtime)
    temp2 = None
    for m in actors:
        temp2 = m

    ia = imdb.IMDb()

    comments = Comment.objects.filter(movie_Id=movie_by_id, active=True)
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
    if temp2:
        if temp2.actor1 != '':
            actorList.append(ia.get_person(temp2.actor1)['name'])
        if temp2.actor2 != '':
            actorList.append(ia.get_person(temp2.actor2)['name'])
        if temp2.actor3 != '':
            actorList.append(ia.get_person(temp2.actor3)['name'])
    print(actorList)
    if 'username' in request.session.keys():
        u = User.objects.filter(username=request.session['username'])[0]
        isLiked = userlikes.objects.filter(movie_id=movie_by_id.id, username=u.username)


    if 'username' in request.session.keys():
        isOrdered = False
        movieOrderList = MovieOrder.objects.filter(username=request.session['username'])
        for m in movieOrderList:
            if str(format(movie_id, '07')) == str(m.movie_Id.id):
                isOrdered = True
                # print(m.movie_Id.title)
                break
        # print(isOrdered)
        print('id', str(format(movie_id, '07')))
        context = {
            'username': request.session['username'],
            'movieData':temp,
            'movieid': str(format(movie_id, '07')),
            'actorList':actorList,
            'movie_detail': movie_by_id,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
            'isLiked': isLiked,
            'isOrdered':isOrdered
        }

        if request.POST:
            return redirect('/movie/' + str(movie_by_id.id))
        else:
            return render(request, 'movie.html', context)
    response = HttpResponse()

    return render(request, 'movie.html', {'movieData':temp,
                                          'movie_detail': movie_by_id,
                                          'comments': comments,
                                          'actorList':actorList
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
    orderList = order.objects.filter(username=request.session['username'])
    # orderList = MovieOrder.objects.filter(username=request.session['username'])
    # movieOrderList = []
    # for m in orderList:
    #     movieOrderList.append(movie.objects.get(id=format(m.movie_Id.id, '07')))
    # print(movieOrderList)
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
        user_email = User.objects.get(username=request.session['username']).email
        username = request.session['username']
        title = request.POST['title']
        subject = 'Thank you for requesting to add a new movie to our database'
        message = ' You have requested to add the following movie to our database ' + request.POST[
            'title'] + ". Thank you for requesting to add a new movie to our database"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = []
        recipient_list.append(user_email)
        htmlmessage = """
            <html lang="en">
    <head>
      <title>Bootstrap Example</title>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
      <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.slim.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
    </head>
    <body>
    <div class="container">

    """ \
                      + " <center><h2>Thank you for your request " + str(username) + " !</h2></center> " \
                                                                                     """
                                                                            
                                                                                  <div class="card">
                                                                                    <div class="card-body" style="text-align: center">
                                                                                      <h4 class="card-title"></h4>
                                                                                      <p class="card-text">Hi, your request to add the title: <strong>
                                                                                      """ + str(title) + "  </strong>" \
                                                                                                         """  
                             to MovieFlix database has been registered successfully. If approved, you would be able to find your requested movie on our website</p>
                           </div>
                         </div>
                       </div>
                       </body>
                       </html>
                               """
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=htmlmessage)
        print(email_from + str(recipient_list) + message + user_email)
        return redirect('/profile')


def likes(request, m_id):
    if 'username' in request.session.keys():
        user = User.objects.get(username=request.session['username'])
        print(user.email)
        movie_title = movie.objects.get(id=format(m_id, '07'))
        print(movie_title)
        userlike = userlikes.objects.filter(username=request.session['username'], movie=movie_title.title)
        print(userlike)
        if not userlike:
            obj = userlikes(movie_id=movie_title, movie=movie_title.title, username=user.username, likes=True)
            obj.save()
            # return redirect('/movie/'+str(m_id))
        else:
            userlike.delete()
        return redirect('/movie/' + str(m_id))
    return redirect('/signin/')


def contact_us(request):
    f = ContactForm()
    context = {
        'form':f
    }
    if 'username' in request.session.keys():
        context['username'] = request.session['username']

    if request.method == 'POST':
        f = ContactForm(request.POST)
        if f.is_valid():
            print(f)
            obj = Contact(name=f.cleaned_data['name'], email=f.cleaned_data['email'], message=f.cleaned_data['message'])
            obj.save()
        context={
            'form': ContactForm(),
        }

    return render(request, 'contact_us.html',context)

def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

def create_checkout_session(request,id):
    id = str(id).rjust(7, '0')
    print(id)
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            movieData = movie.objects.filter(id=id)[0]
            print(movieData.title)
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': movieData.title,
                        'quantity': 1,
                        'currency': 'cad',
                        'amount': str(movieData.price*100),

                    }
                ]
            )
            request.session['id'] = id
            # session_dict['username'] = request.session['username']
            print('keys', request.session.keys())
            return JsonResponse({'sessionId': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
@csrf_exempt
def webhook(request):
    print("Webhook")
    endpoint_secret = settings.ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)


    return HttpResponse(status=200)
def success(request):
    print(request.session.keys())
    print("success")
    movie_order = MovieOrder()
    # print(request.session['id'], request.session['username'])
    movie_order.username = request.session['username']
    movie_order.movie_Id = movie.objects.get(id=request.session['id'])
    movie_order.save()

    user_email = User.objects.get(username=request.session['username']).email
    username = request.session['username']
    subject = 'Thank you for your order'
    message = ' You have ordered the following movie ' + str(movie_order.movie_Id.title)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    recipient_list.append(user_email)
    htmlmessage = """
                <html lang="en">
        <head>
          <title>Bootstrap Example</title>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css">
          <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.0/dist/jquery.slim.min.js"></script>
          <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
          <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js"></script>
        </head>
        <body>
        <div class="container">

        """ \
                  + " <center><h2>Thank you for your order " + str(username) + " !</h2></center> " \
                                                                                 """

                                                                              <div class="card">
                                                                                <div class="card-body" style="text-align: center">
                                                                                  <h4 class="card-title"></h4>
                                                                                  <p class="card-text">Hi, your order for """ + str(movie_order.movie_Id.title) + \
                                                                                   """ has been placed successfully: <strong>
                                                                                   </strong> \
                                                                                                     
                                 </p>
                               </div>
                             </div>
                           </div>
                           </body>
                           </html>
                                   """
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=htmlmessage)
    print(email_from + str(recipient_list) + message + user_email)
    return render(request,'success.html')




class CancelledView(TemplateView):
    template_name = 'cancelled.html'


# def cart_add(request, id):
#     cart = Cart(name)

def MovieOrderList(request):
    print(request.session.keys())
    # if 'username' in session_dict.keys():
    #     movieList = MovieOrder.objects.filter(username=session_dict['username'])
    #     movieOrderList = []
    #     for m in movieList:
    #         movieOrderList.append(m.movie_Id)
    #     print(movieOrderList)
    #     username = session_dict['username']
    #     session_dict.clear()
    #     context = {
    #         'username': username, 'orderList': movieOrderList
    #     }
    #     return render(request, 'movie_order.html', context)

    if 'username' in request.session.keys():
        movieList = MovieOrder.objects.filter(username=request.session['username'])
        movieOrderList = []
        for m in movieList:
            movieOrderList.append(m.movie_Id)
        print(movieOrderList)
        context = {
            'username': request.session['username'], 'orderList': movieOrderList
        }
        return render(request, 'movie_order.html', context)

    return redirect('/signin')