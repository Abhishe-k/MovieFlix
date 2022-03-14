from django.urls import path
from . import views
from .views import registerUser, loginUser, home, logout

urlpatterns = [
    path('home/', home, name='home'),
    path('signup/', registerUser, name='registerUser'),
    path('signin/', loginUser, name='loginUser'),
    path('logout/', logout, name='logout'),
]