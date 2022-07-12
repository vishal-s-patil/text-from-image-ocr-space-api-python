from django.contrib import admin
from django.urls import path
from textfromimage import  views

urlpatterns = [
    path('', views.home, name='home'),
    path('gettextlocal', views.gettextlocal, name='gettextlocal'),
    path('gettexturl', views.gettexturl, name='gettexturl'),
    path('getoverlay', views.getoverlay, name='getoverlay')
]
