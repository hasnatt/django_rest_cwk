from django.urls import path
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('list', views.getAllModules, name = 'getAllModules'),
    path('register', views.register, name = 'register'),
    path('login', views.loginuser, name = 'loginuser'),
    path('logout', views.logoutuser, name = 'logoutuser'),
    path('view', views.viewratings, name = 'viewratings'),
    path('average', views.profaverage, name = 'profaverage'),
    path('rate', views.rateprofessor, name='rateprofessor'),

]
