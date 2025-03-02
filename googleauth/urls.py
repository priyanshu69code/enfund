from django.contrib import admin
from django.urls import path, include
from googleauth import views

urlpatterns = [
    path('google/login/callback/', views.google_callback, name='google_login_callback'),
    path("google/login", views.google_login, name="google_login"),

]
