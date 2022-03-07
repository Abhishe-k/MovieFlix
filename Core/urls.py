from django.urls import path
from . import views
from .views import registerUser, loginUser

urlpatterns = [
    path('signup/',registerUser, name='registerUser'),
    path('signin/',loginUser, name='loginUser'),
]