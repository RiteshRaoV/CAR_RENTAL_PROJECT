from django.shortcuts import redirect
from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('password-reset/', views.password_reset_link, name='password_reset'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_link_check, name='reset_password'),
    path('logout/', views.logout_view, name='logout'),
    path("home/",views.landing_page,name="home")
]
