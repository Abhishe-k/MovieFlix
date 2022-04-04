from django.urls import path
from . import views
from .views import registerUser, loginUser, home, logout, movies, movieDetail, profile_user, order_movie
from movie.views import likes

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('movies/', movies, name='movies'),
    path('movie/<int:movie_id>/', movieDetail, name='movie'),
    path('signup/', registerUser, name='registerUser'),
    path('signin/', loginUser, name='loginUser'),
    path('profile/order/', order_movie, name='Order'),
    path('logout/', logout, name='logout'),
    path('profile/', profile_user, name='profile'),
    path('profile/upload/', views.image_upload, name='upload'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword'),
    path('resetpassword/<int:token>', views.change_password, name='resetpassword'),


]