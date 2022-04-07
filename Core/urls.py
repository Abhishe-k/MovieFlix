from django.urls import path
from . import views
from .views import registerUser, loginUser, home, logout, movies, movieDetail, profile_user, order_movie, contact_us


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
    path('contact/', contact_us, name='contact_us'),
    # path('about_us/', about_us, name='about_us'),
    path('profile/upload/', views.image_upload, name='upload'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword'),
    path('resetpassword/<int:token>', views.change_password, name='resetpassword'),
    path('movies/like/<int:m_id>/', views.likes, name='likes'),
    path('config/', views.stripe_config),
    path('create-checkout-session/<id>', views.create_checkout_session),
    path('success/', views.SuccessView.as_view()), # new
    path('cancelled/', views.CancelledView.as_view()), # new


]