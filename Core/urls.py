from django.urls import path
from . import views
from .views import registerUser, loginUser, home, logout, movies, movieDetail, profile_user

urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('movies/', movies, name='movies'),
    path('movie/<int:movie_id>/', movieDetail, name='movie'),
    path('signup/', registerUser, name='registerUser'),
    path('signin/', loginUser, name='loginUser'),
    path('logout/', logout, name='logout'),
    path('profile/', profile_user, name='profile'),
    path('profile/upload/', views.image_upload, name='upload'),

]