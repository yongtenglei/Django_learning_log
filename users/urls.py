""" define URL model of users """
from django.urls import path, include
from . import views

app_name = 'users'
urlpatterns = [
    # check URL certification by default
    path('', include('django.contrib.auth.urls')),
    # register
    path('register/', views.register, name='register'),
        ]
