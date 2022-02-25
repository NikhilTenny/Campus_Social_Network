from django.contrib import admin
from django.urls import path, include
from .views import home, ProfileView, EditProfileView

urlpatterns = [
    path('home/',home, name='userhome'),
    path('profile/',ProfileView, name='userprofile'),
    path('editprofile/',EditProfileView, name='editprofile')
]